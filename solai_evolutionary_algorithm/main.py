from solai_evolutionary_algorithm.evolution.evolver import Evolver, EvolverConfig
import solai_evolutionary_algorithm.evolve_configurations.test_config as test_config
import solai_evolutionary_algorithm.evolve_configurations.fitness_evaluation_on_existing_character_config as fitness_evaluation_on_existing_character_config


def main():
    evolver = Evolver()
    evolver.evolve(test_config.test_config)
