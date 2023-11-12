# Example usage:
from CityGenerator import CityGenerator
from DamagePredictor import DamagePredictor


if __name__ == "__main__":
    # Create an instance of the CityGenerator class
    city_generator = CityGenerator(size=10)
    city_generator.generate_city()
    city_generator.display_city()

    # Create an instance of the DamagePredictor class with the CityGenerator instance
    damage_predictor = DamagePredictor(city_generator)

    # Build and train the Bayesian network model
    damage_predictor.build_model()
    damage_predictor.train_model()

    # Predict damage for a specific scenario
    evidence = {'Population': 75, 'Age of Building': 25}
    predicted_damage = damage_predictor.predict_damage(evidence)
    print(f'Predicted Damage: {predicted_damage}')