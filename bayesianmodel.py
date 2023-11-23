"""
Bayesian Network Implementation:

This Python script defines classes and methods to construct and perform inference on a Bayesian network. The Bayesian network consists of nodes representing random variables and their dependencies. The script takes input from three JSON files: structure.json, values.json, and queries.json.

- structure.json: Defines the structure of the Bayesian network, including variables and their dependencies.
- values.json: Contains prior and conditional probabilities for the network's variables.
- queries.json: Specifies queries for Bayesian inference.

The code is organized into two main classes:
1. Node: Represents a node in the Bayesian network with methods for initializing, setting probabilities, and retrieving probabilities.
2. BayesianNetwork: Manages the construction and inference of the Bayesian network based on the provided structure, values, and queries.

The main function reads input files, creates a BayesianNetwork instance, constructs the network, and performs inference on the specified queries.

Usage:
python bayesianmodel.py structure.json values.json queries.json
"""

import sys
import json
from itertools import product

class Node(): 

    def __init__(self, name):
        self.parents = []
        self.children = []
        self.name = name
        self.is_prior = True

        # cpt table
        # for prior nodes:
        #     key is variable's value
        # for conditional nodes:
        #     key is a sorted tuple whose item is (variable, variable's value)
        self.prob_table = {}

    def add_child(self, child):
        # Add a child node to the current node.
        self.children.append(child)

    def add_parents(self, parents):
         # Add parent nodes to the current node.
        self.parents.extend(parents)

    def set_is_prior(self, is_prior):
        # Set the is_prior flag for the node.

        self.is_prior = is_prior

    def set_prob_table(self, prob_table):
        # Set the probability table for the node.
        self.prob_table = prob_table

    def is_prior(self):
        return self.is_prior

    def get_prob(self, value_dict):
        if self.is_prior:
            # If the node is a prior node, use the variable's value as the key.
            key = value_dict[self.name]
        else:
            # If the node is conditional, create a sorted tuple with variable-value pairs.
            condition = self.parents + [self.name]
            key = ()
            for c in condition:
                key = key + ((c, value_dict[c]),)
            key = tuple(sorted(key))

        # Retrieve and return the probability from the probability table.
        return self.prob_table[key]


class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []
        self.graph = {}

    def construct_prior_prob_table(self, var):
        
       # Extract the probability values for the prior variable from the input data.
        value_dict = self.prior_probabilities[var]

        # Initialize an empty probability table.
        prob_table = {}

        # Populate the probability table with variable values and their associated probabilities.
        for key in value_dict:
            prob_table[key] = value_dict[key]

        # Return the constructed CPT for the prior variable.
        return prob_table

    def construct_conditional_prob_table(self, var):
       # Extract the conditional probability values for the variable from the input data.
        value_dict_arr = self.conditional_probabilities[var]

        # Initialize an empty probability table.
        prob_table = {}

        # Populate the probability table with variable values and their associated probabilities.
        for value_dict in value_dict_arr:
            prob = value_dict['probability']
            key = ()
            for k in value_dict:
                if k != 'probability':
                    # Include variable-value pairs in the key, excluding 'probability' and 'own_value'.
                    if k != 'own_value':
                        key = key + ((k, value_dict[k]),)
                    else:
                        key = key + ((var, value_dict[k]),)
            key = tuple(sorted(key))
            prob_table[key] = prob

        # Return the constructed CPT for the conditional variable.
        return prob_table

    def construct(self):
        # Initialize nodes for each variable and add them to the graph.
        for var in self.variables:
            node = Node(var)
            self.graph[var] = node

        # Set probability tables and flags for prior nodes.
        for var in self.prior_probabilities:
            self.graph[var].set_prob_table(self.construct_prior_prob_table(var))
            self.graph[var].set_is_prior(True)

        # Set probability tables and flags for conditional nodes, and establish parent-child relationships.
        for var in self.dependencies:
            parents = self.dependencies[var]
            self.graph[var].add_parents(parents)
            self.graph[var].set_prob_table(self.construct_conditional_prob_table(var))
            self.graph[var].set_is_prior(False)
            for p in parents:
                self.graph[p].add_child(var)
        
        # print the graph structure for verification.
        # self.printGraph()

    def infer(self):
        for i in self.queries:
            index = i["index"]
            given = i["given"]
            tofind = i["tofind"]

            # Calculate probability for the given and tofind variables with fixed and varying variables.
            fixed_variables = [x for x in given] + [x for x in tofind]
            varying_variables = [y for y in self.variables if y not in fixed_variables]
            part1 = self.calculate_prob(given, tofind, fixed_variables, varying_variables)

            fixed_variables = [x for x in given]
            varying_variables = list(set([y for y in self.variables if y not in fixed_variables] + [x for x in tofind]))
            part2 = self.calculate_prob(given, tofind, fixed_variables, varying_variables)

            # Calculate the final answer and append it to the answer list.
            answer = part1 / part2
            self.answer.append({"index": index, "answer": answer})
        return self.answer

    def get_every_prob(self, value_dict):
        """
        Get the probability for every variable in the Bayesian network.

        Args:
            value_dict (dict): A dictionary mapping variable names to their values.

        Returns:
            list: A list containing the probabilities for each variable in the network.
        """
        prob_arr = []
        for var in self.graph:
            node = self.graph[var]
            prob_arr.append(node.get_prob(value_dict))
        return prob_arr

    def calculate_prob(self, given, tofind, fixed_variables, varying_variables):
        """
        Calculate the joint probability for given and tofind variables.

        Args:
            given (dict): A dictionary specifying the given variables and their values.
            tofind (dict): A dictionary specifying the variables to find and their values.
            fixed_variables (list): A list of fixed variables.
            varying_variables (list): A list of varying variables.

        Returns:
            float: The calculated joint probability for the given and tofind variables.
        """

        all_prob = []
        table_of_variables = given.copy()
        table_of_variables.update(tofind)
        for var in varying_variables:
            table_of_variables[var] = 'True'
        all_possible_truth_values = self.perm(table_of_variables, len(varying_variables))

        # Iterate over all possible truth values for varying variables.
        for iteration in range(2 ** len(varying_variables)):
            current_truth_values = all_possible_truth_values[iteration]

            # Set the varying variables to their new values.
            for index, var in enumerate(varying_variables):
                table_of_variables[var] = str(current_truth_values[index])

            # Get the probability for each variable and append to the list.
            prob = self.get_every_prob(table_of_variables)
            all_prob.extend([prob])

        # Calculate the final joint probability.
        prob = self.val(all_prob)
        return prob

    def perm(self, tab, length):
        """
        Generate all possible combinations of truth values for a set of variables.

        Args:
            tab (dict): A dictionary of variables and their values.
            length (int): The length of the variable set.

        Returns:
            list: A list of all possible combinations of truth values.
        """
        return list(product([True, False], repeat=length))

    def val(self, arr):
        """
        Calculate the final probability value from the array of individual probabilities.

        Args:
            arr (list): A list of individual probabilities.

        Returns:
            float: The calculated final probability value.
        """
        sum = 0
        for i in arr:
            prod = 1
            for j in i:
                prod *= j
            sum += prod
        return sum

    def printGraph(self):
        for var in self.graph:
            node = self.graph[var]
            print("Node: {} Parent: {} Children: {}".format(node.name, node.parents, node.children))


def main():
    if len(sys.argv) != 4:
        print ("\nUsage: python bayesianmodel.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")

    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()
    
    print(answers)


if __name__ == "__main__":
    main()