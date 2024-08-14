class Neuron:
    def __init__(self, threshold: float, membrane_potential: float = 0.0, dopamine_sensitivity: float = 1.0):
        self.threshold = threshold
        self.membrane_potential = membrane_potential
        self.dopamine_sensitivity = dopamine_sensitivity
        self.synapses = []

    def receive_input(self, input_signal: float, dopamine_level: float = 0.0):
        self.membrane_potential += input_signal * (1 + dopamine_level * self.dopamine_sensitivity)
        if self.membrane_potential >= self.threshold:
            self.fire()
            
    def __repr__(self):
        return f"{self.threshold}, {self.membrane_potential}, {self.synapses}"

    def fire(self):
        self.membrane_potential = 0.0  # Reset potential after firing
        for synapse in self.synapses:
            synapse.transmit_signal()

    def connect_to(self, other_neuron, synapse):
        self.synapses.append(synapse)
        synapse.connect(self, other_neuron)
