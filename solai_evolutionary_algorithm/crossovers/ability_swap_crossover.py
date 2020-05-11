import random
import uuid
from copy import deepcopy
from typing import cast, List
import json

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolution.evolution_types import Individual, SubPopulation
from solai_evolutionary_algorithm.utils.character_id import create_character_id


class AbilitySwapCrossover:
    """
    Swaps a single ability from each parent to produce two children
    """

    def __call__(self, individuals: SubPopulation) -> SubPopulation:
        parents = cast(List[CharacterConfig], individuals)

        abilities_count: int = len(parents[0]['abilities'])
        ability_swap_index: int = (random.randint(0, abilities_count - 1))

        def create_child(my_parent: CharacterConfig, other_parent: CharacterConfig):
            my_parent_abilities = my_parent['abilities']
            other_parent_abilities = other_parent['abilities']

            child_abilities = my_parent_abilities[0: ability_swap_index] \
                + other_parent_abilities[ability_swap_index: ability_swap_index+1] \
                + my_parent_abilities[ability_swap_index+1:]

            return CharacterConfig(
                characterId=create_character_id(),
                radius=my_parent['radius'],
                moveVelocity=my_parent['moveVelocity'],
                abilities=child_abilities
            )

        children = [
            create_child(my_parent, other_parent)
            for my_parent, other_parent in [(parents[0], parents[1]), (parents[1], parents[0])]
        ]

        return children

    def serialize(self):
        config = {
            'description': "Swaps random ability between two parents and produces two children"}
        return config
