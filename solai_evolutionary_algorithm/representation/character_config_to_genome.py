import json
from pkg_resources import resource_stream


def character_config_to_genome(character_config_file):
    genome = []
    data = json.load(resource_stream(
        'solai_evolutionary_algorithm', character_config_file))
    config = data['character_config']
    for att in config:
        genome.append(config[att])
    return genome
