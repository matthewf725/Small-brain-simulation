# brain_creator.py

import pickle
from brain import Brain

def create_and_save_brain(filename="brain.pkl"):
    brain = Brain()
    with open(filename, "wb") as brain_file:
        pickle.dump(brain, brain_file)
    print(f"Brain created and saved to {filename}")

if __name__ == "__main__":
    create_and_save_brain()
