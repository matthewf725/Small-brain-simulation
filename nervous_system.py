class NervousSystem:
    def __init__(self):
        pass

    def encode_text(self, text: str):
        locations = []
        signal_strengths = []
        
        base_strength = 1.0
        attention_boost = 2.0
        context_factor = 0.5
        novelty_boost = 1.5  # Boost for less frequently visited areas

        # Track visits to each location
        location_visits = {}

        for index, char in enumerate(text):
            ascii_value = ord(char)
            
            # Base signal strength inversely proportional to position
            signal_strength = base_strength / (index + 1)
            
            # Contextual influence
            if index > 0:
                signal_strength += context_factor * (ord(text[index - 1]) / 128.0)
            if index < len(text) - 1:
                signal_strength += context_factor * (ord(text[index + 1]) / 128.0)
            
            # Attention boost
            if char.isupper() or char in ['!', '?', '.', ',']:
                signal_strength *= attention_boost
            
            # Track and adjust for location visits
            if ascii_value in location_visits:
                visit_count = location_visits[ascii_value]
                signal_strength /= (visit_count + 1)  # Diminishing returns
            else:
                signal_strength *= novelty_boost  # Boost for new areas

            # Update visit count
            location_visits[ascii_value] = location_visits.get(ascii_value, 0) + 1

            # Append location and adjusted signal strength
            locations.append(ascii_value)
            signal_strengths.append(signal_strength)

        return list(zip(locations, signal_strengths))

