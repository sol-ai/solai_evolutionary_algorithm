from solai_evolutionary_algorithm.mutations.properties_mutation import PropertiesMutation, PropertyMutationData


def default_properties_mutation(
        probability_per_number_property: float = 0.1,
        probability_per_bool_property: float = 0.05
) -> PropertiesMutation:
    return PropertiesMutation(
        character_property_data={
            'radius': PropertyMutationData(
                float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(32, 64)
            ),
            'moveVelocity': PropertyMutationData(
                float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(100, 1200)
            )
        },
        melee_property_data={
            "radius": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(5, 100)
            ),
            "distanceFromChar": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0, 200)
            ),
            "speed": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0, 0)
            ),
            "startupTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "activeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "executionTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "endlagTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "rechargeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0, 60)
            ),
            "damage": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(10, 1000)
            ),
            "baseKnockback": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(10, 1000)
            ),
            "knockbackRatio": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0.1, 1.0)
            ),
            "knockbackPoint": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(-500, 500)
            ),
            "knockbackTowardPoint": PropertyMutationData(
                property_type=bool, probability=probability_per_bool_property,
                mutation_factor_range=(0.5, 1.5), value_range=(False, True)
            )
        },
        projectile_property_data={
            "radius": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(5, 100)
            ),
            "distanceFromChar": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0, 200)
            ),
            "speed": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(100, 800)
            ),
            "startupTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "activeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "executionTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "endlagTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(1, 60)
            ),
            "rechargeTime": PropertyMutationData(
                property_type=int, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0, 60)
            ),
            "damage": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(10, 500)
            ),
            "baseKnockback": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(10, 1000)
            ),
            "knockbackRatio": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(0.1, 1.0)
            ),
            "knockbackPoint": PropertyMutationData(
                property_type=float, probability=probability_per_number_property,
                mutation_factor_range=(0.5, 1.5), value_range=(-500, 500)
            ),
            "knockbackTowardPoint": PropertyMutationData(
                property_type=bool, probability=probability_per_bool_property,
                mutation_factor_range=(0.5, 1.5), value_range=(False, True)
            )
        }
    )