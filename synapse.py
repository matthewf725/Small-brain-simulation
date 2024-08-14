import math

class Synapse:
    def __init__(self, strength: float, dopamine_sensitivity: float = 1.0):
        self.strength = strength
        self.pre_neuron = None
        self.post_neuron = None
        self.activation_count = 0
        self.dopamine_sensitivity = dopamine_sensitivity

    def strengthen(self, dopamine_level: float = 0.0):
        if self.activation_count > 1:
            self.strength += 0.01 * math.log(self.activation_count) * (1 + dopamine_level * self.dopamine_sensitivity)
        else:
            self.strength += 0.01 * (1 + dopamine_level * self.dopamine_sensitivity)
        self.strength = min(self.strength, 1.0)

    def __repr__(self):
        return(f"{self.strength}, {self.pre_neuron}, {self.post_neuron}, {self.activation_count}")

    def connect(self, pre_neuron, post_neuron):
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron

    def transmit_signal(self):
        if self.post_neuron:
            self.post_neuron.receive_input(self.strength)
            self.activation_count += 1
            self.strengthen()