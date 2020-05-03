import random
from copy import deepcopy

from solai_evolutionary_algorithm.evolution.evolution_types import Individual


def __mutate_radius(genome):
    radius = genome['radius']
    max_radius = self.character_config_ranges['radius'][1]
    min_radius = self.character_config_ranges['radius'][0]
    mutation_factor = random.uniform(0.5, 1.5)
    if mutation_factor > 1:
        new_radius = int(min(mutation_factor*radius, max_radius))
    else:
        new_radius = int(max(mutation_factor*radius, min_radius))

    genome['radius'] = new_radius

def __mutate_moveVelocity(genome):
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


def __mutate_ability(ability, melee_ranges, projectile_ranges):
    if ability['type'] == 'melee':
        ranges = melee_ranges
    else:
        ranges = projectile_ranges
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


def __mutate_abilities(genome):
    abilities = genome['abilities']
    for ability in abilities:
        __mutate_ability(ability)


def property_mutation(original_genome: Individual) -> Individual:
    genome = deepcopy(original_genome)
    __mutate_radius(genome)
    __mutate_moveVelocity(genome)
    __mutate_abilities(genome)
    self.representation.change_random_ability_of_character(genome)


def radius_mutation(self, original_genome):
    """
    This mutation scheme only affects the character's radius with a factor ranging from 0.5 to 1.5
    """
    genome = deepcopy(original_genome)
    self.__mutate_radius(genome)
