import math
from typing import Callable, List, Optional, Tuple, Dict, Any
from math import sqrt

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig


def create_character_distance_func(
        character_properties_ranges,
        melee_ability_ranges,
        projectile_ability_ranges
) -> Callable[[CharacterConfig, CharacterConfig], float]:
    def distance_func(char1, char2):
        return normalized_euclidean_distance(
            char1,
            char2,
            character_properties_ranges,
            melee_ability_ranges,
            projectile_ability_ranges
        )
    return distance_func


def normalized_euclidean_distance(
        individual1: CharacterConfig,
        individual2: CharacterConfig,
        character_properties_ranges,
        melee_ability_ranges,
        projectile_ability_ranges
) -> float:

    abilities1 = sorted(individual1['abilities'],
                        key=lambda ability: ability['type'])
    abilities2 = sorted(individual2['abilities'],
                        key=lambda ability: ability['type'])

    character_abilities_normalized_euclidean_distance = 0

    for (ability1, ability2) in zip(abilities1, abilities2):
        if ability1['type'] != ability2['type']:
            character_abilities_normalized_euclidean_distance += len(ability1)
        else:
            if ability1["type"] == "MELEE":
                normalized_ability1 = normalize_dict(
                    ability1, melee_ability_ranges)
                normalized_ability2 = normalize_dict(
                    ability2, melee_ability_ranges)
            else:
                normalized_ability1 = normalize_dict(
                    ability1, projectile_ability_ranges)
                normalized_ability2 = normalize_dict(
                    ability2, projectile_ability_ranges)
            character_abilities_normalized_euclidean_distance += euclidean_distance_dictionary(
                normalized_ability1, normalized_ability2)

    individual1_character_properties = {key: value for (
        key, value) in individual1.items() if key != 'abilities'}
    individual2_character_properties = {key: value for (
        key, value) in individual2.items() if key != 'abilities'}

    individual1_character_properties_normalized = normalize_dict(
        individual1_character_properties, character_properties_ranges)
    individual2_character_properties_normalized = normalize_dict(
        individual2_character_properties, character_properties_ranges)

    character_properties_normalized_euclidean_distance = euclidean_distance_dictionary(
        individual1_character_properties_normalized, individual2_character_properties_normalized)

    distance = character_abilities_normalized_euclidean_distance + character_properties_normalized_euclidean_distance
    if math.isnan(distance):
        raise ValueError(f"calculated distance was NaN for characters: "
                         f"\nCharacter1: {individual1}\nCharacter2: {individual2}")
    return distance


def normalize_dict(dic: Dict, ranges: Dict) -> Dict:
    modified_dict = remove_strings_and_convert_to_floats(dic)
    normalized_dict = {key: normalize(ranges[key][0], ranges[key][1], value) for (
        key, value) in modified_dict.items()}
    return normalized_dict


def normalize(min_value: float, max_value: float, value: float) -> float:
    if (max_value == min_value):
        return 0.0
    else:
        return ((value-min_value)/(max_value-min_value))


def remove_strings_and_convert_to_floats(dic: Dict) -> Dict:
    return {key: float(value) for (key, value) in dic.items() if not isinstance(value, str)}


def euclidean_distance_dictionary(properties1: Dict, properties2: Dict) -> float:
    return sqrt(sum([(properties1[key] - properties2[key]) ** 2 for key in properties2]))
