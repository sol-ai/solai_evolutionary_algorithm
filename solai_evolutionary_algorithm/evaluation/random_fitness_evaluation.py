import random

from solai_evolutionary_algorithm.evolution.evolution_types import FitnessEvaluation, Population, EvaluatedPopulation, \
    EvaluatedIndividual


class RandomFitnessEvaluation(FitnessEvaluation):
    def __call__(self, population: Population) -> EvaluatedPopulation:
        return [
            EvaluatedIndividual(individual=individual, fitness=[random.random()])
            for individual in population
        ]
