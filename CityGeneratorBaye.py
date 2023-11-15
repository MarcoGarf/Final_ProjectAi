import random
import json

class CityGeneratorBaye:
    def __init__(self, size=10):
        self.size = size
        self.city = [['' for _ in range(size)] for _ in range(size)]

    def generate_city(self):
        object_types = ['House', 'Mountain', 'Highway', 'Tall Building', 'School', 'Park', 'Factory']
        materials = ['Concrete', 'Wood', 'Brick']
        ground_types = ['Plain', 'Hill', 'River']

        for i in range(self.size):
            for j in range(self.size):
                object_type = random.choice(object_types)

                if object_type in ['House', 'Tall Building', 'School', 'Factory']:
                    material = random.choice(materials)
                else:
                    material = None

                if object_type in ['House', 'Tall Building', 'School', 'Factory']:
                    population = random.randint(1, 100)
                    age_of_building = random.randint(1, 50)
                    maintenance_factor = random.uniform(0.1, 1.0)
                    ground_type = random.choice(ground_types)

                    if object_type == 'House':
                        num_rooms = random.randint(1, 5)
                        has_garden = random.choice([True, False])
                        has_garage = random.choice([True, False])
                    elif object_type == 'Tall Building':
                        num_floors = random.randint(5, 30)
                        has_elevator = random.choice([True, False])
                    elif object_type == 'School':
                        num_classrooms = random.randint(5, 20)
                        has_playground = random.choice([True, False])
                    elif object_type == 'Factory':
                        production_capacity = random.uniform(100, 1000)
                        has_smokestack = random.choice([True, False])

                elif object_type == 'Mountain':
                    population = 0
                    age_of_building = None
                    maintenance_factor = None
                    ground_type = 'Hill'
                elif object_type == 'Highway':
                    population = 0
                    age_of_building = None
                    maintenance_factor = None
                    ground_type = random.choice(['Plain', 'Hill'])
                elif object_type == 'Park':
                    population = 0
                    age_of_building = None
                    maintenance_factor = None
                    ground_type = random.choice(['Plain', 'Hill', 'River'])

                self.city[i][j] = {
                    'Type': object_type,
                    'Material': material,
                    'Population': population,
                    'Age of Building': age_of_building,
                    'Maintenance Factor': maintenance_factor,
                    'Ground Type': ground_type,
                    'Num Rooms': num_rooms if object_type == 'House' else None,
                    'Has Garden': has_garden if object_type == 'House' else None,
                    'Has Garage': has_garage if object_type == 'House' else None,
                    'Num Floors': num_floors if object_type == 'Tall Building' else None,
                    'Has Elevator': has_elevator if object_type == 'Tall Building' else None,
                    'Num Classrooms': num_classrooms if object_type == 'School' else None,
                    'Has Playground': has_playground if object_type == 'School' else None,
                    'Production Capacity': production_capacity if object_type == 'Factory' else None,
                    'Has Smokestack': has_smokestack if object_type == 'Factory' else None
                }

        # Save the generated city to JSON files
        self.save_to_json()

    def save_to_json(self):
        # Save city information to structure.json
        structure_data = {
            {
            "variables": {
                "Object": ["House", "Mountain", "Highway", "Tall Building", "School", "Park", "Factory"],
                "Material": ["Concrete", "Wood", "Brick"],
                "GroundType": ["Plain", "Hill", "River"],
                "Population": ["Low", "Medium", "High"],
                
                "MaintenanceFactor": ["Low", "Medium", "High"],
                "stories": ["1", "2", "3", "4", "5"],
                "": ["True", "False"],
                "": ["True", "False"],
                "": ["5", "10", "15", "20", "25", "30"],
                "HasElevator": ["True", "False"],
                "NumClassrooms": ["5", "10", "15", "20"],
                "HasPlayground": ["True", "False"],
                "ProductionCapacity": ["Low", "Medium", "High"],
                "": ["True", "False"],

                
                
            },
            "dependencies": {
                damge
                
            }
}

        }
        with open("structure.json", "w") as f:
            json.dump(structure_data, f, indent=2)

        # Save city information to values.json
        values_data = {
            "prior_probabilities": {
                # Modify this based on your generated city structure
            },
            "conditional_probabilities": {
                # Modify this based on your generated city structure
            }
        }
        with open("values.json", "w") as f:
            json.dump(values_data, f, indent=2)

        # Save city information to queries.json
        queries_data = [
            {
                "index": 1,
                "given": {
                    # Modify this based on your generated city structure
                },
                "tofind": {
                    # Modify this based on your generated city structure
                }
            },
            {
                "index": 2,
                "given": {
                    # Modify this based on your generated city structure
                },
                "tofind": {
                    # Modify this based on your generated city structure
                }
            }
        ]
        with open("queries.json", "w") as f:
            json.dump(queries_data, f, indent=2)

    def display_city(self):
        for row in self.city:
            print(row)

if __name__ == "__main__":
    # Create an instance of the CityGenerator class
    city_generator = CityGenerator(size=10)
    city_generator.generate_city()
    city_generator.display_city()
