import os
from datetime import datetime
from typing import Dict
from solai_evolutionary_algorithm.utils.character_distance_utils import create_character_distance_func
from solai_evolutionary_algorithm.evolve_configurations.sol_properties_ranges import character_properties_ranges, melee_ability_ranges, projectile_ability_ranges
from itertools import combinations
import random
from statistics import mean, variance
from math import sqrt

from typing import List
import pymongo


USERNAME = "haraldvinje"
PASSWORD = os.environ["SOLAI_DB_PASSWORD"]
CLUSTER_URL = "mongodb+srv://" + USERNAME + ":" + PASSWORD + \
    "@cluster0-dzimv.mongodb.net/test?retryWrites=true&w=majority"


class ReadOnlyDatabase:

    def __init__(self):
        self.client = pymongo.MongoClient(CLUSTER_URL)
        self.database = self.client.solai
        self.evolution_instances = self.database.evolution_instances

    def get_FINS_with_random_init_pop_instances(self):
        return self.evolution_instances.find({'$and': [{'evolutionConfig.tag_object.infeasible_objective': "FEASIBILITY"},
                                                       {'evolutionConfig.tag_object.initial_population': "random"},
                                                       {"generations.25": {"$exists": "true"}}]},
                                             {'generations'})

    def get_FINS_with_existing_init_pop_instances(self):
        return self.evolution_instances.find({'$and': [{'evolutionConfig.tag_object.infeasible_objective': "FEASIBILITY"},
                                                       {'evolutionConfig.tag_object.initial_population': "from_existing"},
                                                       {"generations.25": {"$exists": "true"}}]},
                                             {'generations'})

    def get_FI2NS_with_random_init_pop_instances(self):
        return self.evolution_instances.find({'$and': [{'evolutionConfig.tag_object.infeasible_objective': "NOVELTY"},
                                                       {'evolutionConfig.tag_object.initial_population': "random"},
                                                       {"generations.25": {"$exists": "true"}}]},
                                             {'generations'})

    def get_FI2NS_with_existing_init_pop_instances(self):
        return self.evolution_instances.find({'$and': [{'evolutionConfig.tag_object.infeasible_objective': "NOVELTY"},
                                                       {'evolutionConfig.tag_object.initial_population': "from_existing"},
                                                       {"generations.25": {"$exists": "true"}}]},
                                             {'generations'})


normalized_euclidean_distance = create_character_distance_func(
    character_properties_ranges=character_properties_ranges,
    melee_ability_ranges=melee_ability_ranges,
    projectile_ability_ranges=projectile_ability_ranges)


def get_last_generation_of_evolution_instance(evolution_instance) -> List:
    return evolution_instance['generations'][-1]


def get_last_feasible_generation_of_evolution_instance(evolution_instance) -> List:
    return filter_feasible_from_population(evolution_instance['generations'][-1])


def filter_feasible_from_population(population):
    return list(filter(lambda individual: individual['feasibility_score'] == 1, population))


def diversity(population):
    return sum([normalized_euclidean_distance(
        char1['individual'],
        char2['individual'])
        for (char1, char2) in combinations(population, 2)])/len(population)


def get_diversity_of_evolution_instance(evolution_instance):
    last_feasible_population = get_last_feasible_generation_of_evolution_instance(
        evolution_instance)
    return diversity(last_feasible_population)


def get_number_of_feasible_of_evolution_instance(evolution_instance):
    last_feasible_population = get_last_feasible_generation_of_evolution_instance(
        evolution_instance)
    return len(last_feasible_population)


def print_statistics_of_evolution(evolution_instances, number_of_evolutions):
    evolution_instances_clone = evolution_instances.clone()
    diversities = [get_diversity_of_evolution_instance(
        evolution_instance) for evolution_instance in evolution_instances][:number_of_evolutions]
    no_of_feasible = [get_number_of_feasible_of_evolution_instance(
        evolution_instance) for evolution_instance in evolution_instances_clone][:number_of_evolutions]
    print(
        f"Average diversity of final populations: {mean(diversities)}")
    print(
        f"Standard deviation diversity of final populations: {sqrt(variance(diversities))}")
    print(
        f"Average number of feasible individuals of final populations: {mean(no_of_feasible)}")
    print(
        f"Standard deviation of feasible individuals of final populations: {sqrt(variance(no_of_feasible))}\n")


print("connecting to DB...")
read_only_db = ReadOnlyDatabase()
print("Connected!\n")

print("getting evolutions")
FINS_w_random_evolutions = read_only_db.get_FINS_with_random_init_pop_instances()
FINS_w_existing_evolutions = read_only_db.get_FINS_with_existing_init_pop_instances()
FI2NS_w_random_evolutions = read_only_db.get_FI2NS_with_random_init_pop_instances()
FI2NS_w_existing_evolutions = read_only_db.get_FI2NS_with_existing_init_pop_instances()
print("evolutions received\n")


print("FINS with random initial population:")
print_statistics_of_evolution(FINS_w_random_evolutions, 20)

print("FINS with existing initial population:")
print_statistics_of_evolution(FINS_w_existing_evolutions, 20)

print("FI2NS with random initial population:")
print_statistics_of_evolution(FI2NS_w_random_evolutions, 20)

print("FI2NS with existing initial population:")
print_statistics_of_evolution(FI2NS_w_existing_evolutions, 20)
