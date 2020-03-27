from solai_evolutionary_algorithm.representation.representation import Representation
from solai_evolutionary_algorithm.evolution.evolution import Evolution
from solai_evolutionary_algorithm.utils.dummy_simulation import DummySimulation
from solai_evolutionary_algorithm.database.database import Database


def main():
    init_poplation_size = 20
    representation = Representation()
    init_population = representation.generate_initial_population(
        init_poplation_size)
    evolution = Evolution()
    evolution.set_initial_population(init_population)
    evolution.evolve()
    fittest_individuals = evolution.get_fittest_individuals()
    return fittest_individuals


def dummy_simulation_with_database():
    init_population_size = 10
    dummy_simulation = DummySimulation(with_database=True)
    dummy_simulation.generate_init_population(init_population_size)
    dummy_simulation.evolve()


def dummy_simulation_without_database():
    init_population_size = 10
    dummy_simulation = DummySimulation(with_database=False)
    dummy_simulation.generate_init_population(init_population_size)
    dummy_simulation.evolve()
