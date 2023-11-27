import itertools
import json

def generate_probabilities(input_data):
    variables = input_data["variables"]
    dependencies = input_data["dependencies"]

    prior_probabilities = {}
    conditional_probabilities = {}

    # Generate prior probabilities
    for variable, values in variables.items():
        prior_probabilities[variable] = {value: 1 / len(values) for value in values}

    # Generate conditional probabilities
    for target_variable, dependent_variables in dependencies.items():
        combinations = list(itertools.product(*[variables[var] for var in dependent_variables]))
        for combination in combinations:
            for own_value in variables[target_variable]:
                probability_key = {var: val for var, val in zip(dependent_variables, combination)}
                probability_key["own_value"] = own_value
                # Convert the hash value of the probability_key to a probability
                hash_value = hash(tuple(probability_key.items()))
                probability_key["probability"] = round(0.01 * (hash_value % 100), 2)
                if target_variable not in conditional_probabilities:
                    conditional_probabilities[target_variable] = []
                conditional_probabilities[target_variable].append(probability_key)

    output = {
        "prior_probabilities": prior_probabilities,
        "conditional_probabilities": conditional_probabilities
    }

    return output

# Input data
input_data = {
    
    "variables": {
         "Building_Collapse": ["True","False"],
         "Earthquake": ["True","False"],
         "IsReinforce": ["True","False"],
         "IsOld": ["True","False"],
         "ConcreteMade" : ["True","False"]
     },
    "dependencies": {
         "Building_Collapse": ["IsReinforce","Earthquake","IsOld"],
         "IsReinforce": ["IsOld"],
         "ConcreteMade" : ["IsOld","IsReinforce"]
     }
 
}

# Generate output
# Generate output
output_data = generate_probabilities(input_data)

# Write the output to a JSON file
with open("output.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("Output written to 'output.json'")
