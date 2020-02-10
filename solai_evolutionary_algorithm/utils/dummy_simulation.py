import json
from ..representation.character_config_to_genome import character_config_to_genome


class DummySimulation:

    solution_filename = "solai_evolutionary_algorithm/representation/interesting_character_for_testing.json"
    solution_genome = None
    init_population = []

    def __init__(self):
        return

    def evaluate_fitness(self, genome):
        return

    def load_interesting_character(self):
        self.init_population.append(
            character_config_to_genome(self.solution_filename))

    def print_init_population_data(self):
        print(self.init_population)
