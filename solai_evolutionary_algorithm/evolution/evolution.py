import copy
import random
from solai_evolutionary_algorithm.socket.character_queue import CharacterQueue
from solai_evolutionary_algorithm.representation.representation import Representation


class Evolution:

    representation = Representation()
    character_config_ranges = representation.character_config
    melee_ranges = representation.melee_config
    projectile_ranges = representation.projectile_config

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
        self.__mutate_radius(genome)
        self.__mutate_moveAccel(genome)
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

    def __mutate_moveAccel(self, genome):
        moveAccel = genome['moveAccel']
        max_moveAccel = self.character_config_ranges['moveAccel'][1]
        min_moveAccel = self.character_config_ranges['moveAccel'][0]
        mutation_factor = random.uniform(0.5, 1.5)
        if mutation_factor > 1:
            new_moveAccel = int(min(mutation_factor*moveAccel, max_moveAccel))
        else:
            new_moveAccel = int(max(mutation_factor*moveAccel, min_moveAccel))

        genome['moveAccel'] = new_moveAccel

    def __mutate_abilities(self, genome):
        abilities = genome['abilities']
        for ability in abilities:
            self.__mutate_ability(abilities[ability])

    def __mutate_ability(self, ability):
        if ability['type'] == 'melee':
            ranges = self.melee_ranges
        else:
            ranges = self.projectile_ranges
        for attribute in ability:
            if attribute == 'type':
                continue
            attribute_value = ability[attribute]

            if type(attribute_value) != bool:
                min_value_attribute = ranges[attribute][0]
                max_value_attribute = ranges[attribute][1]
                mutation_factor = random.uniform(0.5, 1.5)
                if mutation_factor > 1:
                    new_attribute_value = \
                        min(mutation_factor*attribute_value, max_value_attribute)
                else:
                    new_attribute_value = \
                        max(mutation_factor*attribute_value, min_value_attribute)
            else:
                flip_probability = 0.8
                if (random.random() > (1-flip_probability)):
                    print("\n\n\nin the if statement\n\n")
                    new_attribute_value = not attribute_value

            ability[attribute] = new_attribute_value
    """
    --------------------------------------------------------
    End of mutation and crossover section 
    --------------------------------------------------------
    """
