import collections
import json
from pkg_resources import resource_stream


class UsefulFunctions:

    character_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/character_config.json'))['character_config']
    melee_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/melee.json'))
    projectile_config = json.load(resource_stream(
        'solai_evolutionary_algorithm', 'resources/projectile.json'))

    def flatten(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def normalize_genome(self, genome):
        config = self.character_config
        normalized_genome = {}

        min_radius = config["radius"][0]
        max_radius = config["radius"][1]
        radius = genome["radius"]
        normalized_radius = self.normalize(min_radius, max_radius, radius)
        normalized_genome["radius"] = normalized_radius

        min_moveAccel = config["moveAccel"][0]
        max_moveAccel = config["moveAccel"][1]
        moveAccel = genome["moveAccel"]
        normalized_moveAccel = self.normalize(
            min_moveAccel, max_moveAccel, moveAccel)
        normalized_genome["moveAccel"] = normalized_moveAccel

    def normalize(self, min_value, max_value, value):
        return ((value-min_value)/(max_value-min_value))
