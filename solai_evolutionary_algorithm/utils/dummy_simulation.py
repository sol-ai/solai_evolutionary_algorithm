import json
from ..representation.character_config_to_genotype import character_config_to_genotype


class DummySimulation:

    solution_filename = "solai_evolutionary_algorithm/representation/interesting_character_for_testing.json"
    solution_genome = None

    def __init__(self):
        return

    def evaluate_fitness(self, genome):
        return

    def load_interesting_character(self):
        return character_config_to_genotype(self.solution_filename)
