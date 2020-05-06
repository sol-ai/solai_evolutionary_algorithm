import json
import random
import uuid
from copy import deepcopy
from dataclasses import dataclass, asdict
from pkg_resources import resource_stream
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, EvaluatedIndividual


class RandomBoundedProducer(InitialPopulationProducer):
    """
    Generates a random population with properties set randomly given ranges
    """

    @dataclass(frozen=True)
    class Config:
        population_size: int
        character_properties_ranges: any
        melee_ability_ranges: any
        projectile_ability_ranges: any

    ability_types = ["melee", "projectile"]
    no_of_abilities = 3
    character_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/character_config.json'))['character_config']
    melee_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/melee.json'))
    projectile_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/projectile.json'))

    ability_configs = {'melee': melee_config, 'projectile': projectile_config}

    def __init__(self, config: Config):
        self.config = config

    def __call__(self):
        return self.generate_init_population(n=self.config.population_size)

    def generate_init_population(self, n=10):
        return [self.generate_random_character() for _ in range(n)]

    def generate_random_character(self):
        no_of_abilites = self.no_of_abilities
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

    def clone_character(self, genome):
        character_copy = deepcopy(genome)
        character_copy['characterId'] = str(uuid.uuid1())
        return character_copy

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
