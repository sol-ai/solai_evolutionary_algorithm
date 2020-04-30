import sys
import configparser
from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.evolution.evolution import Evolution
from solai_evolutionary_algorithm.utils.dummy_simulation import DummySimulation
from solai_evolutionary_algorithm.database.database import Database
from solai_evolutionary_algorithm.socket.simulation_queue import SimulationQueue


def main(**kwargs):
    poplation_size = 3
    evolution = Evolution(poplation_size, **kwargs)
    evolution.evolve()
    fittest_individuals = evolution.get_fittest_individuals()
    return fittest_individuals


def dummy_simulation(**kwargs):
    init_population_size = 10

    dummy_simulation = DummySimulation(**kwargs)

    dummy_simulation.generate_init_population(init_population_size)
    dummy_simulation.evolve()
