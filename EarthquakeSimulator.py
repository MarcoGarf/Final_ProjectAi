import random

class EarthquakeSimulator:
    @staticmethod
    def simulate_earthquake():
        # Simulate earthquake attributes (magnitude, location, etc.)
        magnitude = random.uniform(4.0, 9.0)
        location = (random.uniform(-90, 90), random.uniform(-180, 180))

        # Other simulation logic...

        return {'Magnitude': magnitude, 'Location': location}