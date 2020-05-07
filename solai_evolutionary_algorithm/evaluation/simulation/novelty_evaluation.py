
#TODO: WIP


def euclidean_distance(genome1, genome2):
    normalized_genome1 = normalize_genome(genome1)
    normalized_genome2 = normalize_genome(genome2)

    genome1_abilities = normalized_genome1['abilities']
    genome2_abilities = normalized_genome2['abilities']

    distance = 0

    for ability1, ability2 in zip(genome1_abilities, genome2_abilities):
        genome1_abilities[ability1]
        distance += euclidean_distance_ability(
            genome1_abilities[ability1], genome2_abilities[ability2])

    return distance


def euclidean_distance_ability(ability1, ability2):
    if ability1['type'] != ability2['type']:
        return 10
    distance = 0
    for attribute in ability1:
        if type(ability1[attribute]) == str:
            continue
        distance += (ability1[attribute] - ability2[attribute])**2
    return distance


def normalize_genome(genome):
    #TODO: implement
    config = {}
    normalized_genome = {}

    min_radius = config["radius"][0]
    max_radius = config["radius"][1]
    radius = genome["radius"]
    normalized_radius = normalize(min_radius, max_radius, radius)
    normalized_genome["radius"] = normalized_radius

    min_moveVelocity = config["moveVelocity"][0]
    max_moveVelocity = config["moveVelocity"][1]
    moveVelocity = genome["moveVelocity"]
    normalized_moveVelocity = normalize(
        min_moveVelocity, max_moveVelocity, moveVelocity)
    normalized_genome["moveVelocity"] = normalized_moveVelocity

    normalized_genome["abilities"] = {}

    for ability in genome["abilities"]:
        genome_ability_config = genome["abilities"][ability]
        ability_config_ranges = ability_configs[genome_ability_config['type']]
        normalized_genome["abilities"][str(ability)] = {}
        normalized_ability_config = {}
        for attribute in genome_ability_config:

            min_attribute_value = ability_config_ranges[str(attribute)][0]
            max_attribute_value = ability_config_ranges[str(attribute)][1]
            attribute_value = genome_ability_config[str(attribute)]
            normalized_attribute_value = normalize(
                min_attribute_value, max_attribute_value, attribute_value)
            normalized_ability_config[attribute] = normalized_attribute_value

        normalized_genome["abilities"][ability] = normalized_ability_config

    return normalized_genome


def normalize(min_value, max_value, value):
    if (max_value == min_value):
        return 0
    if type(value) == str:
        return value
    else:
        return ((value-min_value)/(max_value-min_value))
