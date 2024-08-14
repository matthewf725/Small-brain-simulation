from neuron import Neuron
from synapse import Synapse
class Dopamine:
    def __init__(self, release_threshold: float):
        self.level = 0.0
        self.release_threshold = release_threshold

    def release(self, stimulus_value: float):
        if stimulus_value >= self.release_threshold:
            self.level += (stimulus_value * 0.01)
            # print(f"Dopamine released: {self.level}")

    def decay(self):
        self.level *= 0.65  # Dopamine level decays over time
        print(f"Dopamine decayed: {self.level}")
        
class Hippocampus:
    def __init__(self):
        self.ca1_neurons = [Neuron(threshold=1.0) for _ in range(100)]
        self.ca2_neurons = [Neuron(threshold=1.0) for _ in range(100)]
        self.ca3_neurons = [Neuron(threshold=1.0) for _ in range(100)]
        self.ca4_neurons = [Neuron(threshold=1.0) for _ in range(100)]
        self.dentate_gyrus_neurons = [Neuron(threshold=1.0) for _ in range(100)]

        self.schaffer_collaterals = [Synapse(strength=0.5) for _ in range(100)]
        for i in range(100):
            self.ca3_neurons[i].connect_to(self.ca1_neurons[i], self.schaffer_collaterals[i])
        
        self.dopamine_system = Dopamine(release_threshold=0.5)  # Example threshold

    def process_information(self, encoded_text):
        for (location, signal_strength), neuron in zip(encoded_text, self.dentate_gyrus_neurons):
            self.dopamine_system.release(signal_strength)
            neuron.receive_input(signal_strength, self.dopamine_system.level)
            relevant_neuron = self.ca3_neurons[location % len(self.ca3_neurons)]
            relevant_neuron.receive_input(signal_strength, self.dopamine_system.level)

    def consolidate_memory(self):
        for neuron in self.ca1_neurons:
            neuron.fire()
            for synapse in neuron.synapses:
                synapse.strengthen(self.dopamine_system.level)
        self.dopamine_system.decay()

    def retrieve_memory(self, cue_signal: float):
        for neuron in self.ca3_neurons:
            neuron.receive_input(cue_signal)

        for neuron in self.ca1_neurons:
            neuron.receive_input(cue_signal)

    def neurogenesis(self):
        new_neurons = [Neuron(threshold=1.0) for _ in range(10)]
        self.dentate_gyrus_neurons.extend(new_neurons)
        print("Neurogenesis: New neurons added to the dentate gyrus.")

    def form_new_memory(self, input_signal: float):
        self.process_information(input_signal)
        self.consolidate_memory()

    def custom_print(self):
        print("Hippocampus:")
        print(f"  CA1 Neurons: {self.ca1_neurons}")
        print(f"  CA2 Neurons: {self.ca2_neurons}")
        print(f"  CA3 Neurons: {self.ca3_neurons}")
        print(f"  CA4 Neurons: {self.ca4_neurons}")
        print(f"  Dentate Gyrus Neurons: {self.dentate_gyrus_neurons} neurons")
        print(f"  Schaffer Collaterals: {self.schaffer_collaterals} synapses")
