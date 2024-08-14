# brain_loader.py

import pickle
from brain import Brain

def load_brain(filename="brain.pkl"):
    with open(filename, "rb") as brain_file:
        brain = pickle.load(brain_file)
    return brain

def process_interaction(brain, user_input: str):
    brain.simulate_interaction(user_input)
    brain.save_brain()

if __name__ == "__main__":
    brain = load_brain()
    initial_input = "Hello World!"  # Replace with the actual input
    process_interaction(brain, initial_input)
