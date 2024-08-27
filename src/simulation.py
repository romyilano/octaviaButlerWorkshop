from typing import Callable, List
import tenacity
from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from agents.bidding_dialogue_agent import BiddingDialogueAgent
from agents.dialogue_agent import DialogueAgent
from simulators.dialogue_simulator import DialogueSimulator, select_next_speaker
from utils.character_generator import generate_character_header, generate_character_system_message, generate_character_description
from utils.bid_parser import BidOutputParser, generate_character_bidding_template, ask_for_bid
import os
from dotenv import load_dotenv
import ollama
from langchain_ollama.llms import OllamaLLM

load_dotenv()

model = OllamaLLM(model="llama3.1:latest")

character_names = [
    "Octavia Butler - Science Fiction Writer",
    "Kara Walker - Artist",
    "Aaron Swartz - persecuted entrepreneur and innovator",
    "Zora Neale Hurston - Writer",
    "Jayson - Food not Bombs organizer",
    "Hackerspace members speaking as one - SudoRoom HiveMind"
]

topic = "How do we create hackerspace projects in Oakland at SudoRoom that show the true uniqueness of Oakland in a creative way with leftwing ideals and art so that they are not just the standard hackerspace tech products?"
word_limit = 30

game_description = f"""Here is the topic for the hackerspace topic idea to art critic Jason and hackerspace director Jake: {topic}.
The participants are: {', '.join(character_names)}."""

def initialize_characters():
    character_descriptions = [
        generate_character_description(character_name, game_description, word_limit) for character_name in character_names
    ]
    character_headers = [
        generate_character_header(character_name, character_description, game_description, topic)
        for character_name, character_description in zip(character_names, character_descriptions)
    ]
    character_system_messages = [
        generate_character_system_message(character_name, character_headers, topic, word_limit, character_names)
        for character_name, character_headers in zip(character_names, character_headers)
    ]
    character_bidding_templates = [
        generate_character_bidding_template(character_header)
        for character_header in character_headers
    ]
    
    characters = []
    for character_name, character_system_message, bidding_template in zip(
        character_names, character_system_messages, character_bidding_templates
    ):
        characters.append(
            BiddingDialogueAgent(
                name=character_name,
                system_message=character_system_message,
                model=model,
                bidding_template=bidding_template,
            )
        )
    return characters

def run_simulation(max_iters: int = 20) -> str:
    characters = initialize_characters()
    simulator = DialogueSimulator(agents=characters, selection_function=select_next_speaker)
    simulator.reset()
    
    first_message = "Octavia, Kara, Aaron and Cory, You can now start pitching your ideas for our hackerspace to Jake and the musuem director"
    simulator.inject("Moderator", first_message)
    
    final_dialogue = f"(Moderator): {first_message}\n\n"
    
    for _ in range(max_iters):
        name, message = simulator.step()
        final_dialogue += f"({name}): {message}\n\n"
    
    return final_dialogue

if __name__ == "__main__":
    dialogue = run_simulation()
    print(dialogue)