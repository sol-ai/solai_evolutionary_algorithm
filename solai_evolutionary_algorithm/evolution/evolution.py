from copy import deepcopy
import json
import uuid
import random
from itertools import combinations
import sys
import threading

from solai_evolutionary_algorithm.representation.character_config_to_genome import character_config_to_genome
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.utils.useful_functions import UsefulFunctions
from solai_evolutionary_algorithm.database.database import Database
from solai_evolutionary_algorithm.socket.simulation_queue import SimulationQueue
from solai_evolutionary_algorithm.evaluation.evaluation import Evaluation
from pkg_resources import resource_stream


class Evolution:

    def __init__(self, init_population_size=10, **kwargs):
        self.with_database = kwargs['with_database']
        self.endpoints = kwargs['endpoints']

        self.representation = Representation()
        self.useful_functions = UsefulFunctions()
        self.representation = Representation()

        self.character_config_ranges = self.representation.character_config
        self.melee_ranges = self.representation.melee_config
        self.projectile_ranges = self.representation.projectile_config

        self.init_population = self.generate_init_population(
            init_population_size)

        if self.with_database:
            self.database = Database()

        queue_host = self.endpoints['redis_host']
        queue_port = self.endpoints['redis_port']

        self.simulation_queue = SimulationQueue(
            queue_host, queue_port, init_population_size)

        self.evaluation = Evaluation(self.simulation_queue)

    def generate_init_population(self, n=10):
        init_population = []
        for _ in range(n):
            individual = self.representation.generate_random_character_for_runtime()
            init_population.append(individual)
        return init_population

    def evolve(self):

        current_population = self.init_population
        population_size = len(current_population)

        g = 0

        fitnesses = self.evaluate_one_generation(current_population)
        sorted_fitnesses = sorted((value, key)
                                  for (key, value) in fitnesses.items())

        while g < 2:
            g += 1

            char1_id = sorted_fitnesses[-1][1]
            char2_id = sorted_fitnesses[-2][1]

            char1 = self.get_character_in_population_by_id(
                char1_id, current_population)
            char2 = self.get_character_in_population_by_id(
                char2_id, current_population)

            child = self.crossover_scheme1(char1, char2)

            current_population = [char1, char2]
            remaining = population_size - len(current_population)

            for _ in range(remaining):
                child_clone_mutated = self.representation.clone_character(
                    child)
                self.mutation_scheme1(child_clone_mutated)
                current_population.append(child_clone_mutated)

            fitnesses = self.evaluate_one_generation(current_population)
            sorted_fitnesses = sorted((value, key)
                                      for (key, value) in fitnesses.items())

            print("\n\n-- Generation %i --" % g)
            print(sorted_fitnesses)

        character_and_fitness_configs = []

        for char in sorted_fitnesses:
            fitness = char[0]
            char_id = char[1]
            character_config = self.get_character_in_population_by_id(
                char_id, current_population)
            character_and_fitness_configs.append((fitness, character_config))

        character_and_fitness_configs = character_and_fitness_configs

        self.simulation_queue.push_population(character_and_fitness_configs)

    def evaluate_one_generation(self, population):

        sim_results = self.evaluation.evaluate_one_population(population)
        return sim_results

    def get_fittest_individuals(self):
        return 0

    """
    --------------------------------------------------------
    Define different crossover and mutation functions here
    --------------------------------------------------------
    """

    def crossover_scheme1(self, genome1, genome2):
        new_character = deepcopy(genome1)
        ability_swap_number = (random.randint(0, len(genome1['abilities'])-1))

        genome2_ability = genome2['abilities'][ability_swap_number]
        new_character['abilities'][ability_swap_number] = genome2_ability
        new_character['characterId'] = str(uuid.uuid1())

        return new_character

    def mutation_scheme1(self, genome):
        self.__mutate_radius(genome)
        self.__mutate_moveVelocity(genome)
        self.__mutate_abilities(genome)

    def mutation_scheme2(self, genome):
        """
        This mutation scheme only affects the character's radius with a factor ranging from 0.5 to 1.5
        """
        self.__mutate_radius(genome)

    def __mutate_radius(self, genome):
        radius = genome['radius']
        max_radius = self.character_config_ranges['radius'][1]
        min_radius = self.character_config_ranges['radius'][0]
        mutation_factor = random.uniform(0.5, 1.5)
        if mutation_factor > 1:
            new_radius = int(min(mutation_factor*radius, max_radius))
        else:
            new_radius = int(max(mutation_factor*radius, min_radius))

        genome['radius'] = new_radius

    def __mutate_moveVelocity(self, genome):
        moveVelocity = genome['moveVelocity']
        max_moveVelocity = self.character_config_ranges['moveVelocity'][1]
        min_moveVelocity = self.character_config_ranges['moveVelocity'][0]
        mutation_factor = random.uniform(0.5, 1.5)
        if mutation_factor > 1:
            new_moveVelocity = int(
                min(mutation_factor*moveVelocity, max_moveVelocity))
        else:
            new_moveVelocity = int(
                max(mutation_factor*moveVelocity, min_moveVelocity))

        genome['moveVelocity'] = new_moveVelocity

    def __mutate_abilities(self, genome):
        abilities = genome['abilities']
        for ability in abilities:
            self.__mutate_ability(ability)

    def __mutate_ability(self, ability):
        if ability['type'] == 'melee':
            ranges = self.melee_ranges
        else:
            ranges = self.projectile_ranges
        for attribute in ability:
            if isinstance(ability[attribute], str):
                continue
            attribute_value = ability[attribute]

            if type(attribute_value) != bool:
                min_value_attribute = ranges[attribute][0]
                max_value_attribute = ranges[attribute][1]
                mutation_factor = random.uniform(0.5, 1.5)
                if mutation_factor > 1:
                    new_attribute_value = min(
                        mutation_factor*attribute_value, max_value_attribute)
                else:
                    new_attribute_value = max(
                        mutation_factor*attribute_value, min_value_attribute)
            else:
                flip_probability = 0.2
                if (random.random() > (1-flip_probability)):
                    new_attribute_value = not attribute_value
                else:
                    new_attribute_value = attribute_value

            ability[attribute] = new_attribute_value
    """
    --------------------------------------------------------
    End of mutation and crossover section
    --------------------------------------------------------
    """

    def get_character_in_population_by_id(self, id, population):
        character = None
        for c in population:
            if c['characterId'] == id:
                character = c
        return character
