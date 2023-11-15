from CityGenerator import CityGenerator

if __name__ == "__main__":
   
    city_generator = CityGenerator(size=10)
    city_generator.generate_city()  # Ensure the city is generated before displaying
    city_generator.display_city()
   
    
