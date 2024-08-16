import random
import pickle
from brain import Brain
import numpy as np
from PIL import Image

def load_brain(filename="brain.pkl"):
    with open(filename, "rb") as brain_file:
        brain = pickle.load(brain_file)
    return brain

def process_interaction(brain, user_input: str):
    brain.process_language_input(user_input)
    brain.simulate_interaction(user_input)
    brain.save_brain()

def process_image(brain, image_path: str = "blue.jpg"):
    # Load image and convert to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image).flatten().tolist()
    brain.process_image_input(image_array)
    brain.save_brain()

if __name__ == "__main__":
    brain = load_brain()
    
    # Automatically process the default image
    # process_image(brain)

    # uinput = "User: " + input("User: ")
    # while uinput != "End":
    #     if uinput == "1" or uinput == "2":
    #         brain.adjust_chemicals_based_on_input(uinput)
    #     else:
    #         process_interaction(brain, uinput)
    #     uinput = input("User: ")

    filename = "sentences.txt"
    
    with open(filename, "r") as file:
        lines = file.readlines()
    # print(len(lines))
    for _ in range(100000):  # Loop 100 times
        line = lines[random.randint(0, 6399)]
        if line:
            user_input = line.strip()
            print(f"User: {user_input}")
            process_interaction(brain, user_input)
