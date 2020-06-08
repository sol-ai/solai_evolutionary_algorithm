from solai_evolutionary_algorithm.evolution.evolver import Evolver, EvolverConfig
import solai_evolutionary_algorithm.evolve_configurations.constrained_novelty_config as constrained_novelty_config


def main():
    evolver = Evolver()
    evolver.evolve(constrained_novelty_config.constrained_novelty_config)
