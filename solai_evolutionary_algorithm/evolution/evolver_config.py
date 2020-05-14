from dataclasses import dataclass
from typing import List, Optional

from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, FitnessEvaluation, \
    PopulationEvolver, EndCriteria, EvaluatedPopulation


@dataclass(frozen=True)
class EvolverConfig:
    initial_population_producer: InitialPopulationProducer
    fitness_evaluator: FitnessEvaluation
    population_evolver: PopulationEvolver
    end_criteria: EndCriteria
    evolver_listeners: Optional[List['EvolverListener']] = None


class EvolverListener:

    def on_start(self, config: EvolverConfig):
        pass

    def on_new_generation(self, evaluated_population: EvaluatedPopulation, is_last_generation: bool):
        pass

    def on_end(self):
        pass
