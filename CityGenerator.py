import random

class CityGenerator:
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

    def display_city(self):
        for row in self.city:
            print(row)



