from solai_evolutionary_algorithm.evolution.evolver import Evolver, EvolverConfig
import solai_evolutionary_algorithm.evolve_configurations.test_config as test_config


def main():

    evolver = Evolver()
    evolver.evolve(test_config.test_config)
