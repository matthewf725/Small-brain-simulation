import random
import string
import pickle
from hippocampus import Hippocampus
from nervous_system import NervousSystem

class System2:
    def __init__(self, brain):
        self.brain = brain
        self.context_memory = []
        self.image_context = None

    def follow_signal_path(self, input_text):
        # Encode the text to determine initial signal strengths and corresponding characters
        encoded_text = self.brain.nervous_system.encode_text(input_text)
        
        # Sort by signal strength in descending order
        sorted_text = sorted(encoded_text, key=lambda x: x[1], reverse=True)

        response_chars = []
        current_neurons = []  # Track the neurons involved in the current processing
        current_neuron = self.get_starting_neuron()

        if current_neuron is None:
            return ''  # Return an empty response or handle this case as needed

        while self.can_continue_thinking():
            if current_neuron is None:
                break

            current_neurons.append(current_neuron)  # Add the current neuron to the list

            # Introduce randomness to simulate uncertainty and human-like decisions
            if random.random() < 0.2:  # 20% chance to reconsider the next character
                current_neuron = self.reconsider_neuron_choice(current_neuron)

            # ACC monitors for potential errors more frequently
            if self.brain.ACC.monitor_for_errors(current_neurons):
                self.brain.ACC.increase_focus()
                # Suggest a correction in terms of neuron, not a string
                correction_neuron = self.brain.ACC.suggest_correction(current_neurons)
                if correction_neuron:
                    current_neuron = correction_neuron

            # Determine the character to generate based on current neuron and highest signal
            for ascii_value, strength in sorted_text:
                if current_neuron:
                    if abs(current_neuron.membrane_potential - strength) < 0.1:
                        response_chars.append(chr(ascii_value))
                        self.context_memory.append(current_neuron)  # Store the neuron object
                        self.brain.process_language_input(''.join(response_chars))
                        break

            # Fire the current neuron and move to the next, only if it's valid
            if current_neuron:
                current_neuron.fire()
                next_neuron = self.get_next_neuron(current_neuron)
                if next_neuron:
                    current_neuron = next_neuron
                else:
                    break

        return ''.join(response_chars)

    def get_starting_neuron(self):
        # Logic to find the starting neuron for the signal path
        all_neurons = (self.brain.hippocampus.ca1_neurons + 
                       self.brain.hippocampus.ca2_neurons + 
                       self.brain.hippocampus.ca3_neurons + 
                       self.brain.hippocampus.ca4_neurons)
        
        if not all_neurons:  # Check if the list of neurons is empty
            return None
        
        context_influence = self.calculate_context_influence(all_neurons)
        return max(all_neurons, key=lambda neuron: neuron.membrane_potential + context_influence.get(neuron, 0))

    def get_next_neuron(self, current_neuron):
        # Assuming the neuron connects to others through synapses, find the next neuron to follow
        if not current_neuron or not current_neuron.synapses:
            return None
        
        # Choose the next neuron based on the highest membrane potential among connected neurons
        next_neuron = max(current_neuron.synapses, key=lambda synapse: synapse.post_neuron.membrane_potential).post_neuron
        return next_neuron

    def can_continue_thinking(self):
        # Logic to determine if thinking can continue based on brain chemicals
        dopamine_level = self.brain.hippocampus.dopamine_system.level
        cortisol_level = self.brain.hippocampus.cortisol_system.level

        if dopamine_level < 0.05 or cortisol_level > 0.5:
            return False
        return True

    def reconsider_neuron_choice(self, current_neuron):
        # Reconsider the choice of neuron based on emotional state, context, or ACC feedback
        dopamine_level = self.brain.hippocampus.dopamine_system.level
        cortisol_level = self.brain.hippocampus.cortisol_system.level
        
        if current_neuron:
            if self.brain.ACC.monitor_for_errors([current_neuron]):
                return self.brain.ACC.suggest_correction([current_neuron])

            if dopamine_level > 0.1 and random.random() > 0.5:
                # High dopamine might make the brain more likely to follow optimistic paths
                return self.get_next_highest_signal_neuron(current_neuron)
            elif cortisol_level > 0.3:
                # High cortisol may lead to more cautious thinking, returning to a safer path
                return self.get_previous_neuron(current_neuron)
            else:
                return current_neuron
        return current_neuron  # Return the current neuron if no reconsideration is needed


    def calculate_context_influence(self, neurons):
        # Simulate context influencing neuron selection
        context_influence = {}
        for neuron in neurons:
            influence = random.uniform(0, 0.1)
            if self.image_context:
                # Factor in image context into influence
                influence += self.image_context.get(neuron.ascii_value, 0)
            context_influence[neuron] = influence
        return context_influence

    def get_next_highest_signal_neuron(self, current_neuron):
        # Assuming each neuron is connected to others via synapses
        if not current_neuron.synapses:
            return None
        
        # Trigger the current neuron to fire and propagate signals
        current_neuron.fire()

        # Find the connected neuron with the highest membrane potential after firing
        connected_neurons = [synapse.post_neuron for synapse in current_neuron.synapses]
        if not connected_neurons:
            return None

        next_neuron = max(connected_neurons, key=lambda neuron: neuron.membrane_potential)
        return next_neuron

    def get_previous_neuron(self, current_neuron):
        # Retrieve a neuron that was recently active, simulating reconsideration or second thoughts
        if self.context_memory:
            last_char = self.context_memory.pop()
            encoded_last_char = self.brain.nervous_system.encode_text(last_char)
            matching_neurons = [neuron for neuron in current_neuron.synapses if neuron.membrane_potential == encoded_last_char]
            if matching_neurons:
                return matching_neurons[0]
        return current_neuron

    def update_image_context(self, encoded_image):
        # Store the context of the image as a dictionary for later use
        self.image_context = {ascii_value: membrane_potential for ascii_value, membrane_potential in encoded_image}


class ACC:
    def __init__(self, brain):
        self.brain = brain
        self.error_threshold = 0.0001  # Initial threshold for detecting errors

    def monitor_for_errors(self, current_neurons):
        # Monitor the neurons that are currently selected for processing
        error_detected = False

        # Check the cortisol and dopamine levels of the current neurons
        for neuron in current_neurons:
            neuron_cortisol = neuron.cortisol_level
            neuron_dopamine = self.brain.hippocampus.dopamine_system.level * neuron.dopamine_sensitivity

            if neuron_cortisol > self.error_threshold:
                if random.random() < neuron_cortisol:  # Higher cortisol in the neuron, higher chance of error
                    self.brain.hippocampus.cortisol_system.release(0.5)
                    error_detected = True
                    break
            elif neuron_dopamine < self.error_threshold:
                if random.random() > neuron_dopamine:  # Lower dopamine in the neuron, higher chance of error
                    error_detected = True
                    break

        if error_detected:
            print(f"Error detected in processing neurons. ACC suggests increased focus.")
            return True  # Indicate that an error has been detected
        return False  # No error detected

    def suggest_correction(self, current_neurons):
        # Instead of returning a string, return the neuron itself for correction.
        # We assume that current_neurons is a list of neurons already being processed.

        if current_neurons:
            # Return a neuron with the highest membrane potential or some other condition you want to check
            correction_neuron = max(current_neurons, key=lambda neuron: neuron.membrane_potential)
            return correction_neuron
        else:
            return None  # In case no valid neurons are available for correction

    def increase_focus(self):
        # Increase focus by adjusting error detection thresholds
        self.error_threshold *= 0.9  # Tighten the threshold to reduce errors in the next round
        print(f"ACC: Increasing focus, new error threshold: {self.error_threshold:.3f}")

class Brain:
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.nervous_system = NervousSystem()
        self.system2 = System2(self)
        self.last_neurons = []
        self.ACC = ACC(self)
        self.last_action_dopamine = 0.0

    def generate_response(self, input_text):
        response = self.system2.follow_signal_path(input_text)
        return response

    def respond(self, response):
        dopamine = self.hippocampus.dopamine_system.level
        self.last_neurons = self.system2.context_memory  # Track the neurons involved in the last response
        print(f"{response}", end="")

    def process_language_input(self, text: str):
        encoded_text = self.nervous_system.encode_text(text)
        self.hippocampus.process_information(encoded_text)
        self.hippocampus.consolidate_memory()

    def process_image_input(self, image: list):
        encoded_image = self.nervous_system.encode_image(image)
        self.hippocampus.process_image_information(encoded_image)
        self.hippocampus.consolidate_memory()
        # Update System 2 with image context
        self.system2.update_image_context(encoded_image)

    def simulate_interaction(self, initial_input: str):
        # Process initial input
        self.process_language_input(initial_input)
        while True:
            # Generate and output a response
            response = self.generate_response(initial_input)
            self.respond(response)
            self.process_language_input(response)
            # Decide whether to continue or stop
            if not self.decide_to_continue():
                print("\nBrain: Decided to stop responding.")
                break

    def save_brain(self, filename="brain.pkl"):
        with open(filename, "wb") as brain_file:
            pickle.dump(self, brain_file)

    def adjust_chemicals_based_on_input(self, user_input: int):
        """
        Adjust dopamine or cortisol based on user input.
        If user_input is 1, add dopamine to the last neurons.
        If user_input is 2, add cortisol to the last neurons.
        """
        if user_input == "1":
            # Increase dopamine levels in the last neurons
            for neuron in self.last_neurons:
                neuron.dopamine_sensitivity += 0.01  # Increase dopamine sensitivity
                print(f"Increased dopamine in neuron with ASCII: {neuron.ascii_value}")
        elif user_input == "2":
            # Increase cortisol levels in the last neurons
            for neuron in self.last_neurons:
                neuron.cortisol_level += 0.01  # Increase cortisol level
                print(f"Increased cortisol in neuron with ASCII: {neuron.ascii_value}")
        else:
            print("Invalid input. Please type 1 for dopamine or 2 for cortisol.")

    def decide_to_continue(self):
        ca1_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca1_neurons)
        ca2_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca2_neurons)
        ca3_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca3_neurons)
        ca4_activity = sum(neuron.membrane_potential for neuron in self.hippocampus.ca4_neurons)

        decision_threshold = ca1_activity + ca2_activity + ca3_activity + ca4_activity
        overall_activity = decision_threshold + self.last_action_dopamine - (self.hippocampus.cortisol_system.level * 0.1)

        # print(decision_threshold)
        # print(overall_activity)
        if overall_activity < decision_threshold or decision_threshold == 0 or self.hippocampus.dopamine_system.level < 0.05:
            return False  # Decide to stop
        return True  # Decide to continue
