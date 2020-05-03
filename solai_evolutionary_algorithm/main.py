from solai_evolutionary_algorithm.evolution.evolution import Evolution
from solai_evolutionary_algorithm.evolution.evolver import Evolver, EvolverConfig
from solai_evolutionary_algorithm.utils.dummy_simulation import DummySimulation
import solai_evolutionary_algorithm.evolve_configurations.test_config as test_config

def main(**kwargs):

    evolver = Evolver()
    evolver.evolve(test_config.test_config)

    # poplation_size = 3
    # evolution = Evolution(poplation_size, **kwargs)
    # evolution.evolve()
    # fittest_individuals = evolution.get_fittest_individuals()
    # return fittest_individuals


def dummy_simulation(**kwargs):
    init_population_size = 10

    dummy_simulation = DummySimulation(**kwargs)

    dummy_simulation.generate_init_population(init_population_size)
    dummy_simulation.evolve()
