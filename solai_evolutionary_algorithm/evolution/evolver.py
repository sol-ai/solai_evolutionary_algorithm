from dataclasses import dataclass

from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, FitnessEvaluation, \
    PopulationEvolver, EndCriteria, Population, EvaluatedPopulation
from solai_evolutionary_algorithm.database.database import Database


class FixedGenerationsEndCriteria:
    def __init__(self, generations: int):
        self.generations = generations
        self.curr_generation = 0

    def __call__(self) -> bool:
        self.curr_generation += 1
        return self.curr_generation >= self.generations


@dataclass(frozen=True)
class EvolverConfig:
    initial_population_producer: InitialPopulationProducer
    fitness_evaluator: FitnessEvaluation
    population_evolver: PopulationEvolver
    end_criteria: EndCriteria
    database: Database


class Evolver:
    def __init__(self):
        pass

    def evolve(self, config: EvolverConfig):

        config.database.init_evolution_instance()
        initial_population: Population = config.initial_population_producer()

        curr_population = initial_population
        generation = 0
        while True:
            print(f"Starting generation {generation}")
            evaluated_population: EvaluatedPopulation = config.fitness_evaluator(
                curr_population)
            new_population: Population = config.population_evolver(
                evaluated_population)

            config.database.add_character_generation(new_population)
            if config.end_criteria():
                break

            generation += 1

            curr_population = new_population

        config.database.end_evolution_instance()
