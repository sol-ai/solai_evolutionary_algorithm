import json


def character_config_to_genome(character_config_file):
    genome = []
    with open(character_config_file, 'r') as character:
        data = json.load(character)
        config = data['character_config']
        for att in config:
            genome.append(config[att])
    return genome
