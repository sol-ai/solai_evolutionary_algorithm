from dataclasses import dataclass
from typing import List, Optional, Tuple, Callable

from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, FitnessEvaluation, \
    PopulationEvolver, EndCriteria, Population, EvaluatedPopulation
from solai_evolutionary_algorithm.evolution.evolver_listener import EvolverListener


@dataclass(frozen=True)
class EvolverConfig:
    initial_population_producer: InitialPopulationProducer
    fitness_evaluator: FitnessEvaluation
    population_evolver: PopulationEvolver
    end_criteria: EndCriteria
    evolution_listeners: Optional[List[EvolverListener]] = None


class Evolver:
    def __init__(self):
        pass

    def evolve(self, config: EvolverConfig) -> Tuple[Population, EvaluatedPopulation]:
        initial_population: Population = config.initial_population_producer()

        generation = 0
        curr_population: Population = initial_population
        evaluated_population: EvaluatedPopulation

        if config.evolver_listeners:
            for listener in config.evolver_listeners:
                listener.on_start(config)

        while True:
            print(f"Starting generation {generation}")
            evaluated_population = config.fitness_evaluator(curr_population)

            is_last_generation = config.end_criteria()

            if config.evolver_listeners:
                for listener in config.evolver_listeners:
                    listener.on_new_generation(
                        evaluated_population, is_last_generation)

            if is_last_generation:
                break

            new_population: Population = config.population_evolver(
                evaluated_population)

            generation += 1

            curr_population = new_population

        return curr_population, evaluated_population
