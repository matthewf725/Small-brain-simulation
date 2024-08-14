import random
import string
import pickle
from hippocampus import Hippocampus
from nervous_system import NervousSystem

class Brain:
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.nervous_system = NervousSystem()
        self.last_action_dopamine = 0.0

    def decide_to_continue(self):
        ca1_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca1_neurons)
        ca2_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca2_neurons)
        ca3_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca3_neurons)
        ca4_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca4_neurons)

        decision_threshold = ca1_activity + ca2_activity + ca3_activity + ca4_activity
        overall_activity = decision_threshold + self.last_action_dopamine - (self.hippocampus.cortisol_system.level * 0.1)
        # print("\n")
        # print(overall_activity/400.0)
        # print(decision_threshold)
        # print(self.hippocampus.dopamine_system.level)
        if overall_activity / 400.0 < decision_threshold and self.hippocampus.dopamine_system.level < 0.05:
            return False  # Decide to stop
        return True  # Decide to continue

    def generate_response(self):
        # Cortisol might influence response generation (e.g., more erratic under high stress)
        # if self.hippocampus.cortisol_system.level > 0.5:
        #     response_length = max(1, response_length - int(self.hippocampus.cortisol_system.level * 5))
        response = ''.join(random.choice(string.ascii_letters) for _ in range(1))
        return response

    def respond(self, response: str):
        # Process the generated response, reinforcing dopamine and memory consolidation
        self.process_language_input(response)
        self.last_action_dopamine = self.hippocampus.dopamine_system.level
        print(f"{response}", end="")

    def process_language_input(self, text: str):
        encoded_text = self.nervous_system.encode_text(text)
        self.hippocampus.process_information(encoded_text)
        self.hippocampus.consolidate_memory()

    def simulate_interaction(self, initial_input: str):
        # Process initial input
        self.process_language_input(initial_input)
        response = self.generate_response()
        self.respond(response)

        while True:
            # Generate and output a response
            response = self.generate_response()
            self.respond(response)

            # Decide whether to continue or stop
            # input("Enter to continue")
            if not self.decide_to_continue():
                print("\nBrain: Decided to stop responding.")
                break

    def save_brain(self, filename="brain.pkl"):
        with open(filename, "wb") as brain_file:
            pickle.dump(self, brain_file)
