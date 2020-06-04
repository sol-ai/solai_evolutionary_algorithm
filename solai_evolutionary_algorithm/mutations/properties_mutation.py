import random
from copy import deepcopy
from dataclasses import dataclass, asdict
from numbers import Number
from typing import Dict, Any, List, cast, Tuple, Callable, Optional, TypeVar, Type

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig, AbilityConfig
from solai_evolutionary_algorithm.evolution.evolution_types import Individual
from solai_evolutionary_algorithm.evolution.generation_evolver import Mutation
from solai_evolutionary_algorithm.utils.character_id import create_character_id


def __clamp(value: Number, value_range: Tuple[Number, Number]):
    """
    range is a list of two numbers: [min, max]
    """
    return max(value_range[0], min(value_range[1], value))


PropertyMutator = Callable[[Any, Tuple[float, float], Tuple[Any, Any]], Any]


def mutate_float_property(
    value: float,
    mutation_factor_range: Tuple[float, float],
    value_range: Tuple[float, float]
) -> float:
    mutation_factor = random.uniform(
        mutation_factor_range[0], mutation_factor_range[1])
    new_radius = mutation_factor * value
    new_radius_bound = __clamp(new_radius, value_range)
    return cast(float, new_radius_bound)


def mutate_int_property(
        value: int,
        mutation_factor_range: Tuple[float, float],
        value_range: Tuple[int, int]
) -> int:
    return int(mutate_float_property(value, mutation_factor_range, value_range))


def mutate_bool_property(
        value: bool,
        mutation_factor_range: Tuple[float, float],
        value_range: Tuple[bool, bool],
) -> bool:
    """
    Returns the opposite value, ignoring mutation_factor_range and value_range.
    Bool properties should in general be converted to a number that can be converted to a bool when evaluated
    """
    return not value


# TypeVar("PropertyType", Type[float], Type[int], Type[bool])
PropertyType = Any


@dataclass(frozen=True)
class PropertyMutationData:
    property_type: PropertyType
    probability: float  # in the range [0, 1]
    mutation_factor_range: Tuple[float, float]
    value_range: Optional[Tuple[Any, Any]] = None


def mutate_property(value: PropertyType, mutation_data: PropertyMutationData) -> PropertyType:
    if mutation_data.property_type == float:
        return mutate_float_property(value, mutation_data.mutation_factor_range, mutation_data.value_range)
    elif mutation_data.property_type == int:
        return mutate_int_property(value, mutation_data.mutation_factor_range, mutation_data.value_range)
    elif mutation_data.property_type == bool:
        return mutate_bool_property(value, mutation_data.mutation_factor_range, mutation_data.value_range)
    else:
        raise ValueError(
            f"Mutation property of type {mutation_data.property_type} is not supported")


def mutate_property_with_probability(value: PropertyType, mutation_data: PropertyMutationData):
    if random.random() < mutation_data.probability:
        return mutate_property(value, mutation_data)
    else:
        return value


def mutate_ability(
    ability: AbilityConfig,
    properties_probability: Dict[str, float],
    mutation_factor_range: Tuple[float, float],
    melee_property_ranges: Dict[str, Tuple[Any, Any]],
    projectile_property_ranges: Dict[str, Tuple[Any, Any]],
) -> AbilityConfig:
    mutateable_properties_with_type = {
        "radius": float,
        "distanceFromChar": float,
        "speed": float,
        "startupTime": int,
        "activeTime": int,
        "executionTime": int,
        "endlagTime": int,
        "rechargeTime": int,
        "damage": float,
        "baseKnockback": float,
        "knockbackRatio": float,
        "knockbackPoint": float,
        "knockbackTowardPoint": bool
    }

    property_mutators_by_type: Dict[Any, PropertyMutator] = {
        float: mutate_float_property,
        int: mutate_int_property,
        bool: mutate_bool_property
    }

    use_property_ranges: Dict[str, Tuple[Any, Any]
                              ] = projectile_property_ranges if ability['type'] == 'PROJECTILE' else melee_property_ranges

    def mutate_ability_property(prop_name: str) -> Any:
        probability = properties_probability[prop_name]
        value = ability[prop_name]

        if random.random() < probability:
            prop_type = mutateable_properties_with_type[prop_name]
            mutate_func = property_mutators_by_type[prop_type]
            value_range = use_property_ranges[prop_name]
            mutate_func(value, mutation_factor_range, value_range)
        else:
            return value

    mutated_properties = {
        prop_name: mutate_ability_property(prop_name)
        for prop_name in mutateable_properties_with_type
    }

    mutated_ability: AbilityConfig = {
        'name': ability['name'],
        'type': ability['type'],
        **mutated_properties
    }
    return mutated_ability


def mutate_character(
    char: CharacterConfig,
    character_property_data: Dict[str, PropertyMutationData],
    melee_property_data: Dict[str, PropertyMutationData],
    projectile_property_data: Dict[str, PropertyMutationData]
):
    char_mutated_props = {
        prop_name: mutate_property_with_probability(
            value=char[prop_name],
            mutation_data=prop_data
        )
        for prop_name, prop_data in character_property_data.items()
    }

    abilities_mutated_props = [
        {
            prop_name: mutate_property_with_probability(
                value=ability[prop_name],
                mutation_data=prop_data
            )
            for prop_name, prop_data in (
                melee_property_data if ability['type'] == 'MELEE' else projectile_property_data
            ).items()
        }
        for ability in char['abilities']
    ]

    mutated_char: CharacterConfig = {
        **char,
        'characterId': create_character_id(),
        **char_mutated_props,
        'abilities': [
            {
                **ability,
                **mutated_ability_props
            }
            for ability, mutated_ability_props in zip(char['abilities'], abilities_mutated_props)
        ]
    }
    return mutated_char


@dataclass
class PropertiesMutation(Mutation):
    character_property_data: Dict[str, PropertyMutationData]
    melee_property_data: Dict[str, PropertyMutationData]
    projectile_property_data: Dict[str, PropertyMutationData]

    def __call__(self, original_genome: Individual) -> Individual:
        char_config = cast(CharacterConfig, original_genome)
        mutated_char_config: CharacterConfig = mutate_character(
            char_config,
            character_property_data=self.character_property_data,
            melee_property_data=self.melee_property_data,
            projectile_property_data=self.projectile_property_data
        )

        return mutated_char_config

    def serialize(self) -> Dict:
        dic = str(asdict(self))
        return dic


def print_mutations(
        char_config,
        mutated_char_config,
        character_property_data,
        melee_property_data,
        projectile_property_data
):
    def print_change(prop_name: str, orig_value, new_value, begin_with: str = ""):
        if orig_value == new_value:
            print(f"{begin_with}{prop_name}: {new_value}")
        else:
            print(f"{begin_with}{prop_name}: {orig_value} -> {new_value}")

    for char_prop in character_property_data:
        print_change(
            char_prop, char_config[char_prop], mutated_char_config[char_prop])

    for i, (mutated_ability, orig_ability) in enumerate(zip(mutated_char_config['abilities'], char_config['abilities'])):
        print(f"ability{i}: {mutated_ability['name']}")
        for ability_prop in melee_property_data:
            print_change(
                ability_prop, orig_ability[ability_prop], mutated_ability[ability_prop], begin_with="\t")
