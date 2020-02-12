import json
from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.utils.useful_functions import UsefulFunctions
from pkg_resources import resource_stream


class DummySimulation:

    solution_genome = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/sample_characters/interesting_character_for_testing.json'))
    init_population = []
    useful_functions = UsefulFunctions()

    def __init__(self):
        self.representation = Representation()
        return

    def evaluate_fitness(self, genome):
        return

    def generate_init_population(self, n=10):
        for _ in range(n):
            individual = self.representation.generate_random_character_for_runtime()
            self.init_population.append(individual)

    def print_init_population_data(self):
        for individual in self.init_population:
            print("\n", individual, "\n")
        print("\n", self.solution_genome, "\n")

    def dummy_fitness_function(self, genome):
        return 0

    def euclidean_distance(self, genome1, genome2):
        normalize_genome = self.useful_functions.normalize_genome
        flatten = self.useful_functions.flatten

        flat_genome1 = flatten(genome1)
        flat_genome2 = flatten(genome2)
        genome1_list = list(flat_genome1.values())
        genome2_list = list(flat_genome2.values())

    def test_euclidean_distance(self):
        test_genome1 = self.init_population[0]
        test_genome2 = self.init_population[1]
        self.euclidean_distance(test_genome1, test_genome2)
