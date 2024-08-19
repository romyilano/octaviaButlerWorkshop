# Session2: Octavia Butler Open Source AI Meetup RAG and Vector Databases 

* https://lu.ma/m3qsibqb

We Continue our Open-Source AI workshop from last week with a focus on Vector Databases and RAG with inspiration from Octavia Butler, science fiction goddess.

​We will focus of course on open-sourced models and also see if it’s not too hard to get an open-sourced generative AI model on a raspberry pi for hardware hacking projects.

![image](session_01/images/Butler-Perret_BACK-ofbook-1.jpg)





## Basics
We're using open-source models with the Ollama open-source framework

- Download [Ollama](https://www.ollama.com)

- At the command line run ollama (depends on which computer you have, open the ollama app on a mac and run a command on debian linux, will update)

- List the models you have downloaded to your computer
```
ollama list

```

## handling the virtual environment
Don't get your python libraries all dirty! Isolate them in the directory for this project 

```
python -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

## about this meetup

The purpose of this [Octavia Butler Open-Source AI meetup](https://sudoroom.org/inspiration-from-goat-octavia-butler/) is to get our hands dirty with code and face-to-face interaction at the SudoRoom hackerspace in Oakland. AI is coming our way for all its good or bad qualities, but we should be proactive and try to figure out way to deal with it humanely.


* From the first session [https://sudoroom.org/inspiration-from-goat-octavia-butler/](https://sudoroom.org/inspiration-from-goat-octavia-butler/)