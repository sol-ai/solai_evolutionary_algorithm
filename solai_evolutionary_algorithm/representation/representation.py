import json
import random
import uuid
import os
from pkg_resources import resource_stream


class Representation:

    ability_types = ["melee", "projectile"]
    no_of_abilities = 3
    character_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/character_config.json'))['character_config']
    melee_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/melee.json'))
    projectile_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/projectile.json'))

    def generate_initial_population(self, n):
        return 0

    def generate_random_character_file(self):
        new_character = self.generate_random_character()
        file_name = "character_" + new_character["characterId"] + ".json"
        path = "./sample_characters/"
        with open(path + file_name, 'w', encoding='utf-8') as output_file:
            json.dump(new_character, output_file, ensure_ascii=False, indent=4)

    def generate_random_character_for_runtime(self):
        new_character = self.generate_random_character()
        return new_character

    def generate_random_character(self):
        no_of_abilites = self.no_of_abilities
        new_character = {}
        new_character["characterId"] = str(uuid.uuid1())
        config = self.character_config

        min_radius = config["radius"][0]
        max_radius = config["radius"][1]
        radius = random.randint(min_radius, max_radius)
        new_character["radius"] = radius

        min_moveAccel = config["moveAccel"][0]
        max_moveAccel = config["moveAccel"][1]
        moveAccel = random.randint(min_moveAccel, max_moveAccel)
        new_character["moveAccel"] = moveAccel

        for i in range(no_of_abilites):
            new_character["ability" +
                          str(i+1)] = self.__generate_random_ability()

        return new_character

    def __generate_random_ability(self):
        ability_type = self.ability_types[random.randint(
            0, len(self.ability_types)-1)]
        if ability_type == "melee":
            return self.__generate_random_melee_ability()
        if ability_type == "projectile":
            return self.__generate_random_projectile_ability()

    def __generate_random_melee_ability(self):
        melee_ability = {}
        data = self.melee_config
        melee_ability["type"] = data["type"]
        for attribute in data:
            if attribute not in melee_ability:
                min_value = data[attribute][0]
                max_value = data[attribute][1]
                if type(min_value) == int:
                    melee_ability[attribute] = random.randint(
                        min_value, max_value)
                elif type(min_value) == float:
                    melee_ability[attribute] = random.uniform(
                        min_value, max_value)
                elif type(min_value) == bool or type(min_value) == str:
                    no_values = len(data[attribute])
                    melee_ability[attribute] = data[attribute][random.randint(
                        0, no_values-1)]
            return melee_ability

    def __generate_random_projectile_ability(self):
        projectile_ability = {}
        data = self.projectile_config
        projectile_ability["type"] = data["type"]
        for attribute in data:
            if attribute not in projectile_ability:
                min_value = data[attribute][0]
                max_value = data[attribute][1]
                if type(min_value) == int:
                    projectile_ability[attribute] = random.randint(
                        min_value, max_value)
                elif type(min_value) == float:
                    projectile_ability[attribute] = random.uniform(
                        min_value, max_value)
                elif type(min_value) == bool or type(min_value) == str:
                    no_values = len(data[attribute])
                    projectile_ability[attribute] = data[attribute][random.randint(
                        0, no_values-1)]

        return projectile_ability
