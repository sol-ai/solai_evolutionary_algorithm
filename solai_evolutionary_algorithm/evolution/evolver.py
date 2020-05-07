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

    def serialize(self):
        return {'description': f'Ends after {self.generations} generations are produced'}


GenerationsListener = Callable[[Population, EvaluatedPopulation, bool], None]


class EvolutionListener:

    def on_start(self, config):
        pass

    def on_new_generation(self, new_popoulation, is_last_generation):
        pass

    def on_end(self):
        pass


@dataclass(frozen=True)
class EvolverConfig:
    initial_population_producer: InitialPopulationProducer
    fitness_evaluator: FitnessEvaluation
    population_evolver: PopulationEvolver
    end_criteria: EndCriteria
    evolution_listeners: Optional[List[EvolutionListener]] = None


class Evolver:
    def __init__(self):
        pass

    def evolve(self, config: EvolverConfig) -> Tuple[Population, EvaluatedPopulation]:
        initial_population: Population = config.initial_population_producer()

        generation = 0
        curr_population: Population = initial_population
        evaluated_population: EvaluatedPopulation

        if config.evolution_listeners is not None:
            for listener in config.evolution_listeners:
                listener.on_start(config)

        while True:
            print(f"Starting generation {generation}")
            evaluated_population = config.fitness_evaluator(curr_population)

            is_last_generation = config.end_criteria()

            if config.evolution_listeners is not None:
                for listener in config.evolution_listeners:
                    listener.on_new_generation(
                        evaluated_population, is_last_generation)

            if is_last_generation:
                break

            new_population: Population = config.population_evolver(
                evaluated_population)

            generation += 1

            curr_population = new_population

        return curr_population, evaluated_population
