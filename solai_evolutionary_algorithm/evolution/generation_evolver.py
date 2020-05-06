import math
import numbers
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import Callable, List, Optional

from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, SubPopulation, \
    Individual, EvaluatedIndividual

Crossover = Callable[[SubPopulation], SubPopulation]
Mutation = Callable[[Individual], Individual]
IndividualProducer = Callable[[], Individual]


class DefaultGenerationEvolver:
    """
    This generation evolver first orders individuals given an EvaluatedPopulationOrderer.
    Then the
    Assuming bi-crossovers that take two individuals and produces two individuals
    Then applies the given Mutators to all children
    """

    @dataclass(frozen=True)
    class Config:
        crossover_share: float
        elitism_share: float
        new_individuals_share: float
        crossover: Optional[Crossover] = None
        mutations: Optional[List[Mutation]] = None
        new_individuals_producer: Optional[IndividualProducer] = None

    PassThroughConfig = Config(
        crossover_share=0,
        elitism_share=1,
        new_individuals_share=0
    )

    def __init__(self, config: Config):
        self.config = config

        if self.config.crossover_share != 0 and not config.crossover:
            raise ValueError("No crossover provided and crossover_share not 0")

        if self.config.new_individuals_share != 0 and not config.new_individuals_producer:
            raise ValueError(
                "No new_individual_producer provided and new_individuals_share not 0")

    def __call__(self, evaluated_population: EvaluatedPopulation) -> Population:
        def fitness_retriever(evaluated_individual: EvaluatedIndividual):
            fitness = evaluated_individual['fitness']
            if type(fitness) == list and len(fitness) > 0 and isinstance(fitness[0], numbers.Number):
                return sum(fitness)
            else:
                raise ValueError(
                    "fitness must be a list of at least one float")

        ordered_evaluated_population = sorted(
            evaluated_population,
            key=fitness_retriever,
            reverse=True
        )

        ordered_population = [
            evaluated_individual['individual']
            for evaluated_individual in ordered_evaluated_population
        ]
        population_count = len(ordered_evaluated_population)

        individuals_amount = self._share2amount(
            population_count,
            [self.config.crossover_share, self.config.elitism_share,
                self.config.new_individuals_share]
        )
        if sum(individuals_amount) != population_count:
            raise ValueError(
                "Percentages does not add up to produce an equal sized population")

        crossover_count, elitism_count, new_individuals_count = individuals_amount

        if crossover_count % 2 != 0:
            raise ValueError(
                "Crossover amount does not add up to an even number given the population size")

        individuals_to_be_crossed = ordered_population[:crossover_count]
        individual_pairs_to_be_crossed = [
            individuals_to_be_crossed[i: i+2]
            for i in range(0, len(individuals_to_be_crossed), 2)
        ]
        crossover_children = list(chain.from_iterable(
            self.config.crossover(individual_pair)
            for individual_pair in individual_pairs_to_be_crossed
        ))

        elitism_individuals = ordered_population[:elitism_count]
        new_individuals = [self.config.new_individuals_producer()
                           for _ in range(new_individuals_count)]

        new_population = crossover_children + elitism_individuals + new_individuals

        def mutate(individual: Individual) -> Individual:
            mutated_individual = reduce(
                lambda prev_individual, new_mutation: new_mutation(
                    prev_individual),
                self.config.mutations,
                individual
            )
            return mutated_individual

        new_mutated_population = [
            mutate(individual)
            for individual in new_population
        ] if (self.config.mutations is not None) else new_population

        return new_mutated_population

    @staticmethod
    def _share2amount(total: int, shares: List[float]) -> List[int]:
        return [
            round(total * x)
            for x in shares
        ]

    def serialize(self):
        config = {'crossoverShare': self.config.crossover_share,
                  'newIndividualsShare': self.config.new_individuals_share}
        if self.config.crossover:
            config['crossover'] = self.config.crossover.serialize()
        if self.config.mutations:
            config['mutations'] = [mutation.serialize()
                                   for mutation in self.config.mutations]
        return config
