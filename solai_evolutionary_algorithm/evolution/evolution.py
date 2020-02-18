import copy
import random
from solai_evolutionary_algorithm.socket.character_queue import CharacterQueue


class Evolution:

    def evolve(self):
        offspring = None

    def get_fittest_individuals(self):
        return 0

    def set_initial_population(self, init_population):
        self.init_populatio = init_population

    """
    --------------------------------------------------------
    Define different crossover and mutation functions here
    --------------------------------------------------------
    """

    def crossover_scheme1(self, genome1, genome2):
        new_character = copy.deepcopy(genome1)
        ability_swap_number = 'ability' + \
            str(random.randint(1, len(genome1['abilities'])))

        genome2_ability = genome2['abilities'][ability_swap_number]
        new_character['abilities'][ability_swap_number] = genome2_ability

        return new_character

    def mutation_scheme1(self, genome):
        return genome

    """
    --------------------------------------------------------
    End of mutation and crossover section 
    --------------------------------------------------------
    """
