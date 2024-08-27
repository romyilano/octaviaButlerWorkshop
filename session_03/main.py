from typing import Callable, List
import tenacity

from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

from agents.bidding_dialogue_agent import BiddingDialogueAgent
from agents.dialogue_agent import DialogueAgent
from simulators.dialogue_simulator import DialogueSimulator
from utils.character_generator import generate_character_header, generate_character_system_message, generate_character_description
from utils.bid_parser import BidOutputParser, generate_character_bidding_template, ask_for_bid
from simulators.dialogue_simulator import DialogueSimulator, select_next_speaker
import os
from dotenv import load_dotenv
import ollama
from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="llama3.1:latest")

# Define your characters, topic, and word limit here
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
character_descriptions = [
    generate_character_description(character_name, game_description, word_limit) for character_name in character_names
]
character_headers = [
    generate_character_header(character_name, character_description, game_description, topic)
    for character_name, character_description in zip(
        character_names, character_descriptions
    )
]
character_system_messages = [
    generate_character_system_message(character_name, character_headers, topic, word_limit, character_names)
    for character_name, character_headers in zip(character_names, character_headers)
]


print("Testing BiddingDialogueAgent")
characters = []

character_bidding_templates = [
    generate_character_bidding_template(character_header)
    for character_header in character_headers
]

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
 
# debugging hack in python
# for agent in characters:
#     print(f"\nAll attributes of {agent.name}'s BiddingDialogueAgent:")
#     for key, value in vars(agent).items():
#         print(f"{key}: {value}")


max_iters = 20
n = 0

simulator = DialogueSimulator(agents=characters, selection_function=select_next_speaker)
simulator.reset()

first_message = "Octavia, Kara, Aaron and Cory, You can now start pitching your ideas for our hackerspace to Jake and the musuem director"
simulator.inject("Moderator", first_message )
print(f"(Moderator): {first_message}")
print("\n")

final_dialogue = ""

while n < max_iters:
    name, message = simulator.step()
    print(f"({name}): {message}")
    print("\n")
    final_dialogue += f"({name}): {message}"
    final_dialogue += "\n"
    n += 1

print(final_dialogue)
