import json
import operator
from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.utils.useful_functions import UsefulFunctions
from solai_evolutionary_algorithm.evolution.evolution import Evolution
from pkg_resources import resource_stream


class DummySimulation:

    solution_genome = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/sample_characters/interesting_character_for_testing.json'))['character_config']
    init_population = []
    generation_pool = []

    useful_functions = UsefulFunctions()
    representation = Representation()
    evolution = Evolution()

    def evolve(self):
        fitnesses = self.evaluate_fitness_of_population()
        sorted_fitnesses = sorted((value, key)
                                  for (key, value) in fitnesses.items())

        g = 0

        char1_id = sorted_fitnesses[-1][1]
        char2_id = sorted_fitnesses[-2][1]

        char1 = self.get_character_by_id(char1_id)
        char2 = self.get_character_by_id(char2_id)

        new_char = self.evolution.crossover_scheme1(char1, char2)
        new_char_copy = self.representation.copy_character_new_id(new_char)
        self.evolution.mutation_scheme1(new_char_copy)

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
        i = 0
        for individual in self.init_population:
            i += 1
            print("\n", "individual no", i, "\n", individual, "\n")
        print("\n", self.solution_genome, "\n")

    def dummy_fitness_function(self, genome):
        return 100-self.representation.euclidean_distance(self.solution_genome, genome)

    def get_character_by_id(self, id):
        character = None
        for c in self.init_population:
            if c['characterId'] == id:
                character = c
        return character
