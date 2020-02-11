import json
from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from pkg_resources import resource_stream


class DummySimulation:

    solution_file = 'resources/sample_characters/interesting_character_for_testing.json'
    solution_genome = None
    init_population = []

    def __init__(self):
        self.representation = Representation()
        return

    def evaluate_fitness(self, genome):
        return

    def load_interesting_character(self):
        self.solution_genome = character_config_to_genome(
            self.solution_file)

    def generate_init_population(self, n=10):
        for _ in range(n):
            individual = self.representation.generate_random_character_for_runtime()
            self.init_population.append(individual)

    def print_init_population_data(self):
        for individual in self.init_population:
            print("\n", individual, "\n")
