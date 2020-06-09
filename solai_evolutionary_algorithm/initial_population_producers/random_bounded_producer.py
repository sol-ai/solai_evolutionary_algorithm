import json
import random
import uuid
from copy import deepcopy
from dataclasses import dataclass, asdict
from pkg_resources import resource_stream
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, EvaluatedIndividual, \
    Individual


class RandomBoundedProducer(InitialPopulationProducer):
    """
    Generates a random population with properties set randomly given ranges
    """

    @dataclass(frozen=True)
    class Config:
        character_properties_ranges: any
        melee_ability_ranges: any
        projectile_ability_ranges: any
        no_of_abilities: int = 3

    def __init__(self, config: Config):
        self.config = config
        self.character_config = config.character_properties_ranges
        self.ability_configs = {'melee': config.melee_ability_ranges,
                                'projectile': config.projectile_ability_ranges}
        self.ability_types = list(self.ability_configs.keys())
        self.no_of_abilites = config.no_of_abilities

    def __call__(self):
        return self.generate_random_character()

    def generate_init_population(self, n=10):
        return [self.generate_random_character() for _ in range(n)]

    def generate_random_character(self) -> Individual:
        no_of_abilites = self.no_of_abilites
        new_character = {}
        new_character["characterId"] = str(uuid.uuid4())
        config = self.character_config

        min_radius = config["radius"][0]
        max_radius = config["radius"][1]
        radius = random.randint(min_radius, max_radius)
        new_character["radius"] = radius

        min_moveVelocity = config["moveVelocity"][0]
        max_moveVelocity = config["moveVelocity"][1]
        moveVelocity = random.randint(min_moveVelocity, max_moveVelocity)
        new_character["moveVelocity"] = moveVelocity
        new_character["abilities"] = []

        for _ in range(no_of_abilites):
            new_character["abilities"].append(self.__generate_random_ability())

        return new_character

    def __generate_random_ability(self):
        ability_type = self.ability_types[random.randint(
            0, len(self.ability_types)-1)]
        return self.__generate_random_ability_by_type(ability_type)

    def __generate_random_ability_by_type(self, ability_type):
        ability = {}
        data = self.ability_configs[ability_type]
        ability["type"] = data["type"]
        for attribute in data:
            if attribute not in ability:
                min_value = data[attribute][0]
                max_value = data[attribute][1]
                if type(min_value) == int:
                    ability[attribute] = random.randint(
                        min_value, max_value)
                elif type(min_value) == float:
                    ability[attribute] = random.uniform(
                        min_value, max_value)
                elif type(min_value) == bool or type(min_value) == str:
                    no_values = len(data[attribute])
                    ability[attribute] = data[attribute][random.randint(
                        0, no_values-1)]

        return ability

    def serialize(self):
        return asdict(self.config)
