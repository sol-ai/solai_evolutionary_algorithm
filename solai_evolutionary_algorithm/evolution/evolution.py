import copy
import random
from solai_evolutionary_algorithm.socket.character_queue import CharacterQueue
from solai_evolutionary_algorithm.representation.representation import Representation


class Evolution:

    representation = Representation()
    character_config_ranges = representation.character_config
    melee_ranges = representation.melee_config
    projectile_config = representation.projectile_config

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
        """
        This mutation scheme only affects the character's radius with a factor ranging from 0.5 to 1.5
        """
        radius = genome['radius']
        max_radius = self.character_config_ranges['radius'][1]
        min_radius = self.character_config_ranges['radius'][0]
        mutation_factor = random.uniform(0.5, 1.5)
        if mutation_factor > 1:
            new_radius = int(min(mutation_factor*radius, max_radius))
        else:
            new_radius = int(max(mutation_factor*radius, min_radius))

        genome['radius'] = new_radius

    """
    --------------------------------------------------------
    End of mutation and crossover section 
    --------------------------------------------------------
    """
