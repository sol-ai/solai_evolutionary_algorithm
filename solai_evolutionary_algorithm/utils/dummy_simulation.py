import json
import operator
import pprint
from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.utils.useful_functions import UsefulFunctions
from pkg_resources import resource_stream


class DummySimulation:

    solution_genome = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/sample_characters/interesting_character_for_testing.json'))['character_config']
    init_population = []
    useful_functions = UsefulFunctions()
    representation = Representation()

    def __init__(self):
        self.representation = Representation()

    def evolve(self):
        fitnesses = self.evaluate_fitness_of_population()

        g = 0

        max_fitness_char_id = max(
            fitnesses.items(), key=operator.itemgetter(1))[0]
        char = self.get_character_by_id(max_fitness_char_id)

    def evaluate_fitness_of_population(self):
        population = self.init_population
        fitnesses = {}
        for individual in population:
            fitnesses[individual['characterId']] = self.dummy_fitness_function(
                individual)
        return fitnesses

    def generate_init_population(self, n=10):
        for _ in range(n):
            individual = self.representation.generate_random_character_for_runtime()
            self.init_population.append(individual)

    def print_init_population_data(self):
        for individual in self.init_population:
            print("\n", individual, "\n")
        print("\n", self.solution_genome, "\n")

    def dummy_fitness_function(self, genome):
        return 100-self.representation.euclidean_distance(self.solution_genome, genome)

    def get_character_by_id(self, id):
        character = None
        for c in self.init_population:
            if c['characterId'] == id:
                character = c
        return character
