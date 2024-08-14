class Neuron:
    def __init__(self, threshold: float, membrane_potential: float = 0.0, 
                 dopamine_sensitivity: float = 1.0, cortisol_sensitivity: float = 1.0):
        self.threshold = threshold
        self.membrane_potential = membrane_potential
        self.dopamine_sensitivity = dopamine_sensitivity
        self.cortisol_sensitivity = cortisol_sensitivity
        self.synapses = []
        self.cortisol_level = 0.0  # Initialize cortisol level

    def receive_input(self, input_signal: float, dopamine_level: float = 0.0, cortisol_level: float = 0.0):
        self.cortisol_level = cortisol_level
        # Cortisol can make it harder to reach threshold (by increasing the threshold)
        effective_threshold = self.threshold * (1 + self.cortisol_level * self.cortisol_sensitivity)
        # Dopamine can make it easier for the neuron to fire
        self.membrane_potential += input_signal * (1 + dopamine_level * self.dopamine_sensitivity)
        if self.membrane_potential >= effective_threshold:
            self.fire()
            
    def __repr__(self):
        return f"Threshold: {self.threshold}, Membrane Potential: {self.membrane_potential}, Synapses: {self.synapses}, Cortisol Level: {self.cortisol_level}"

    def fire(self):
        self.membrane_potential = 0.0  # Reset potential after firing
        for synapse in self.synapses:
            synapse.transmit_signal()

    def connect_to(self, other_neuron, synapse):
        self.synapses.append(synapse)
        synapse.connect(self, other_neuron)
