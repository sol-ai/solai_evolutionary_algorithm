import random
import uuid
from copy import deepcopy

from solai_evolutionary_algorithm.evolution.evolution_types import Individual, SubPopulation


def ability_swap_crossover(self, individuals: SubPopulation):
    """
    Swaps a single ability from each parent
    TODO: crossovers should yield two children
    """
    [genome1, genome2] = individuals
    new_character = deepcopy(genome1)
    ability_swap_number = (random.randint(0, len(genome1['abilities'])-1))

    genome2_ability = genome2['abilities'][ability_swap_number]
    new_character['abilities'][ability_swap_number] = genome2_ability
    new_character['characterId'] = str(uuid.uuid4())

    new_character2 = deepcopy(new_character)

    return [new_character, new_character2]
