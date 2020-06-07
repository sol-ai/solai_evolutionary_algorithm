
from solai_evolutionary_algorithm.mutations.random_new_ability_mutation import RandomNewAbilityMutation, PropertyMutationData
from typing import Dict


def default_random_new_ability_mutation(
        character_properties_ranges: Dict[str, tuple],
        melee_ability_ranges: Dict[str, tuple],
        projectile_ability_ranges: Dict[str, tuple],
        probability_per_number_property: float = 0.5,
        probability_per_bool_property: float = 0.05,
        probability_for_random_new_ability: float = 0.1

) -> RandomNewAbilityMutation:
    return RandomNewAbilityMutation(
        random_new_ability_probability=probability_for_random_new_ability,
        character_property_data={
            key: PropertyMutationData(
                float,
                probability=probability_per_number_property,
                mutation_factor_range=(0.8, 1.2),
                value_range=property_range
            )
            for (key, property_range) in character_properties_ranges.items()
        },
        melee_property_data={
            "radius": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges['radius']
            ),
            "distanceFromChar": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["distanceFromChar"]
            ),
            "speed": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["speed"]
            ),
            "startupTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["startupTime"]
            ),
            "activeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["activeTime"]
            ),
            "executionTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["executionTime"]
            ),
            "endlagTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["endlagTime"]
            ),
            "rechargeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["rechargeTime"]
            ),
            "damage": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["damage"]
            ),
            "baseKnockback": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["baseKnockback"]
            ),
            "knockbackRatio": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["knockbackRatio"]
            ),
            "knockbackPoint": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["knockbackPoint"]
            ),
            "knockbackTowardPoint": PropertyMutationData(
                property_type=bool, probability=probability_per_bool_property,
                mutation_factor_range=(0.5, 1.5), value_range=melee_ability_ranges["knockbackTowardPoint"]
            )
        },
        projectile_property_data={
            "radius": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["radius"]
            ),
            "distanceFromChar": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["distanceFromChar"]
            ),
            "speed": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["speed"]
            ),
            "startupTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["startupTime"]
            ),
            "activeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["activeTime"]
            ),
            "executionTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["executionTime"]
            ),
            "endlagTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["endlagTime"]
            ),
            "rechargeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["rechargeTime"]
            ),
            "damage": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["damage"]
            ),
            "baseKnockback": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["baseKnockback"]
            ),
            "knockbackRatio": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["knockbackRatio"]
            ),
            "knockbackPoint": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["knockbackPoint"]
            ),
            "knockbackTowardPoint": PropertyMutationData(
                property_type=bool, probability=probability_per_bool_property,
                mutation_factor_range=(0.5, 1.5), value_range=projectile_ability_ranges["knockbackTowardPoint"]
            )
        }
    )
