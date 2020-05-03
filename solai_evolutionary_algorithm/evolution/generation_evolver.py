import math
from dataclasses import dataclass
from functools import reduce
from typing import Callable, List, Optional

from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, SubPopulation, \
    Individual

EvaluatedPopulationOrderer = Callable[[EvaluatedPopulation], EvaluatedPopulation]


Crossover = Callable[[SubPopulation], SubPopulation]
Mutation = Callable[[Individual], Individual]
IndividualProducer = Callable[[], Individual]


@dataclass(frozen=True)
class DefaultGenerationEvolver:
    """
    This generation evolver first orders individuals given an EvaluatedPopulationOrderer.
    Then the
    Assuming bi-crossovers that take two individuals and produces two individuals
    Then applies the given Mutators to all children
    """

    population_orderer: EvaluatedPopulationOrderer
    crossover_share: float
    elitism_share: float
    new_individuals_share: float
    crossover: Optional[Crossover]
    mutations: Optional[List[Mutation]]
    new_individuals_producer: Optional[IndividualProducer]

    def __init__(self):
        if self.crossover_share != 0 and not self.crossover:
            raise ValueError("No crossover provided and crossover_share not 0")

        if self.new_individuals_share != 0 and not self.new_individuals_producer:
            raise ValueError("No new_individual_producer provided and new_individuals_share not 0")

    def __call__(self, evaluated_population: EvaluatedPopulation) -> Population:
        ordered_evaluated_population = self.population_orderer(evaluated_population)
        ordered_population = [
            evaluated_individual['individual']
            for evaluated_individual in ordered_evaluated_population
        ]
        population_count = len(ordered_evaluated_population)

        individuals_amount = self._share2amount(
            population_count,
            [self.crossover_share, self.elitism_share, self.new_individuals_share]
        )
        if sum(individuals_amount) != population_count:
            raise ValueError("Percentages does not add up to produce an equal sized population")

        crossover_count, elitism_count, new_individuals_count = individuals_amount

        if crossover_count % 2 != 0:
            raise ValueError("Crossover amount does not add up to an even number given the population size")

        crossover_individuals = ordered_population[:crossover_count]
        elitism_individuals = ordered_population[:elitism_count]
        new_individuals = [self.new_individuals_producer() for _ in range(new_individuals_count)]

        new_population = crossover_individuals + elitism_individuals + new_individuals

        def mutate(individual: Individual) -> Individual:
            mutated_individual = list(reduce(
                lambda prev_individual, new_mutation: new_mutation(prev_individual),
                self.mutations,
                individual
            ))
            return mutated_individual

        new_mutated_population = [
            mutate(individual)
            for individual in new_population
        ]
        return new_mutated_population

    @staticmethod
    def _share2amount(total: int, shares: List[float]) -> List[int]:
        return [
            round(total * x)
            for x in shares
        ]
