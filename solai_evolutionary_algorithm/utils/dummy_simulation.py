import operator
import json
import time
from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.utils.useful_functions import UsefulFunctions
from solai_evolutionary_algorithm.evolution.evolution import Evolution
from solai_evolutionary_algorithm.database.database import Database
from solai_evolutionary_algorithm.socket.character_queue import CharacterQueue
from pkg_resources import resource_stream


class DummySimulation:

    def __init__(self, **kwargs):
        self.with_database = kwargs['with_database']
        self.solution_genome = json.load(resource_stream(
            'solai_evolutionary_algorithm', 'resources/sample_characters/interesting_character_for_testing.json'))['character_config']
        self.init_population = []
        self.useful_functions = UsefulFunctions()
        self.representation = Representation()
        self.evolution = Evolution()

        if self.with_database:
            self.database = Database()
            self.character_queue = CharacterQueue()

    def evolve(self):

        current_population = self.init_population
        population_size = len(current_population)
        fitnesses = self.evaluate_fitness_of_population(current_population)
        sorted_fitnesses = sorted((value, key)
                                  for (key, value) in fitnesses.items())

        g = 0

        while g < 1000:
            g += 1
            print("\n\n-- Generation %i --" % g)

            char1_id = sorted_fitnesses[-1][1]
            char2_id = sorted_fitnesses[-2][1]

            char1 = self.get_character_in_population_by_id(
                char1_id, current_population)
            char2 = self.get_character_in_population_by_id(
                char2_id, current_population)

            child = self.evolution.crossover_scheme1(char1, char2)

            current_population = [char1, char2]
            remaining = population_size - len(current_population)

            for _ in range(remaining):
                child_clone_mutated = self.representation.clone_character(
                    child)
                self.evolution.mutation_scheme1(child_clone_mutated)
                current_population.append(child_clone_mutated)

            if self.with_database:
                self.database.add_dummy_generation(current_population, g)
                self.character_queue.push_character_pair(char1, char2)

            fitnesses = self.evaluate_fitness_of_population(current_population)
            sorted_fitnesses = sorted((value, key)
                                      for (key, value) in fitnesses.items())
            print(sorted_fitnesses)

        print(200*"=")
        print(5*"\n")
        print("Evolution done")
        print(5*"\n")

        if self.with_database:
            print("Last generation", self.database.get_generation(g))
            self.database.close_connection()

        print(200*"=")
        print(5*"\n")

    def evaluate_fitness_of_population(self, population):
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
        for index, individual in enumerate(self.init_population):
            print("\n", "individual no", index, "\n", individual, "\n")

    def dummy_fitness_function(self, genome):
        return 100-self.representation.euclidean_distance(self.solution_genome, genome)

    def get_character_in_population_by_id(self, id, population):
        character = None
        for c in population:
            if c['characterId'] == id:
                character = c
        return character
