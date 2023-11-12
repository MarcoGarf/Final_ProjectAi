import random

from CityGenerator import CityGenerator
from DamagePredictor import DamagePredictor

class BayesianNetworkSimulator:
    def __init__(self):
        self.city_generator = CityGenerator()
        self.damage_predictor = DamagePredictor()

    def simulate_network(self):
        self.city_generator.generate_city()
        self.city_generator.display_city()

        city_data = self.city_generator.city
        self.damage_predictor.build_model(city_data)
        self.damage_predictor.train_model(city_data)

        # Example: Predict damage for a specific scenario
        evidence = {'Population': 50, 'Age of Building': 20}
        predicted_damage = self.damage_predictor.predict_damage(evidence)
        print(f'Predicted Damage: {predicted_damage}')


