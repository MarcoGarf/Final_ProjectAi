import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import ParameterEstimator
from pgmpy.inference import VariableElimination

class DamagePredictor:
    def __init__(self, city_generator):
        self.model = None
        self.city_generator = city_generator

    def build_model(self):
        # Access city data directly from the CityGenerator instance
        city_data = self.city_generator.city

        # Ensure that there is at least one row of data
        if not city_data or not city_data[0]:
            raise ValueError("City data is empty")

        # Check if city_data is a list of dictionaries or a 2D list of dictionaries
        if isinstance(city_data[0], dict):
            # If it's a list of dictionaries, extract the keys from the first dictionary
            keys = list(city_data[0].keys())
        else:
            # If it's a 2D list of dictionaries, flatten it and extract the keys from the first dictionary
            flattened_city_data = [item for sublist in city_data for item in sublist]
            keys = list(flattened_city_data[0].keys())

        # Define nodes and edges based on the city_data attributes
        edges = [(key, 'Damage') for key in keys]  # Create edges for each attribute to 'Damage'

        # Create a Bayesian model
        self.model = BayesianModel(edges)


    def train_model(self):
        # Access city data directly from the CityGenerator instance
        city_data = self.city_generator.city

        # Ensure that there is at least one row of data
        if not city_data or not city_data[0]:
            raise ValueError("City data is empty")

        # Flatten the 2D list of dictionaries into a list of dictionaries
        flattened_city_data = [item for sublist in city_data for item in sublist]

        # Convert flattened_city_data to a Pandas DataFrame
        data = pd.DataFrame(flattened_city_data)

        # Fit the model parameters using Maximum Likelihood Estimation
        self.model.fit(data, estimator=ParameterEstimator)

    def predict_damage(self, evidence):
        # Perform variable elimination to predict damage based on evidence
        infer = VariableElimination(self.model)
        predicted_damage = infer.map_query(variables=['Damage'], evidence=evidence)
        return predicted_damage['Damage']
