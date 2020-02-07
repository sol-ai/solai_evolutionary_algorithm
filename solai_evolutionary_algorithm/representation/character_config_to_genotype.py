import json


def character_config_to_genotype(character_config_file):
    genotype_vector = []
    with open(character_config_file, 'r') as character:
        data = json.load(character)
        config = data['character_config']
        for att in config:
            genotype_vector.append(config[att])
    return genotype_vector
