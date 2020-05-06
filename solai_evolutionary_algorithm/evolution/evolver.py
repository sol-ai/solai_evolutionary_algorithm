from dataclasses import dataclass
from typing import List, Optional, Tuple, Callable

from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, FitnessEvaluation, \
    PopulationEvolver, EndCriteria, Population, EvaluatedPopulation


class FixedGenerationsEndCriteria:
    def __init__(self, generations: int):
        self.generations = generations
        self.curr_generation = 0

    def __call__(self) -> bool:
        self.curr_generation += 1
        return self.curr_generation >= self.generations


GenerationsListener = Callable[[Population, EvaluatedPopulation, bool], None]


@dataclass(frozen=True)
class EvolverConfig:
    initial_population_producer: InitialPopulationProducer
    fitness_evaluator: FitnessEvaluation
    population_evolver: PopulationEvolver
    end_criteria: EndCriteria
    generation_listeners: Optional[List[GenerationsListener]] = None


class Evolver:
    def __init__(self):
        pass

    def evolve(self, config: EvolverConfig) -> Tuple[Population, EvaluatedPopulation]:
        initial_population: Population = config.initial_population_producer()

        generation = 0
        curr_population: Population = initial_population
        evaluated_population: EvaluatedPopulation

        while True:
            print(f"Starting generation {generation}")
            evaluated_population = config.fitness_evaluator(curr_population)

            is_last_generation = config.end_criteria()

            if config.generation_listeners is not None:
                for listener in config.generation_listeners:
                    listener(curr_population, evaluated_population, is_last_generation)

            if is_last_generation:
                break

            new_population: Population = config.population_evolver(evaluated_population)

            generation += 1

            curr_population = new_population

        return curr_population, evaluated_population
