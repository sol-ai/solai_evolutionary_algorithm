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
    A generation evolver that first orders individuals by the sum of their fitnesses.
    Then children and new individuals will be produced and mutated,
    forming the new generation with the elitism individuals
    """

    @dataclass(frozen=True)
    class Config:
        # Percent in the range [0, 1] of the best individuals that will be crossed to form children,
        # based on the crossover function.
        # Must be a percent that yields an even number of individuals
        crossover_share: float

        # Percent in the range [0, 1] of the best individuals that will be mutated and carried to the next generation
        mutate_only_share: float

        # Percent in the range [0, 1] of the worst individuals that will be replaced by new individuals
        # given by the new_individuals_producer
        new_individuals_share: float

        # Percent in the range [0, 1] of the best individuals that will be carried to the next generation
        # without mutation
        elitism_share: float

        crossover: Optional[Crossover] = None
        mutations: Optional[List[Mutation]] = None
        new_individuals_producer: Optional[IndividualProducer] = None

    PassThroughConfig = Config(
        crossover_share=0,
        mutate_only_share=0,
        elitism_share=1,
        new_individuals_share=0
    )

    def __init__(self, config: Config):
        self.config = config

        if self.config.crossover_share != 0 and not config.crossover:
            raise ValueError("No crossover provided and crossover_share not 0")

        if self.config.new_individuals_share != 0 and not config.new_individuals_producer:
            raise ValueError("No new_individual_producer provided and new_individuals_share not 0")

    def __call__(self, evaluated_population: EvaluatedPopulation) -> Population:
        def fitness_retriever(evaluated_individual: EvaluatedIndividual):
            fitness = evaluated_individual['fitness']
            if type(fitness) == list and len(fitness) > 0 and isinstance(fitness[0], numbers.Number):
                return sum(fitness)
            else:
                raise ValueError("fitness must be a list of at least one float")

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

        raw_crossover_count = self._share2amount(population_count, self.config.crossover_share)
        if raw_crossover_count % 2 != 0:
            print(f"Crossover count rounded down to be even, from: {raw_crossover_count}")
            crossover_count = raw_crossover_count - 1
        else:
            crossover_count = raw_crossover_count

        mutate_only_count = self._share2amount(population_count, self.config.mutate_only_share)
        new_individuals_count = self._share2amount(population_count, self.config.new_individuals_share)
        elitism_count = self._share2amount(population_count, self.config.elitism_share)

        individuals_to_be_crossed = ordered_population[:crossover_count]
        individual_pairs_to_be_crossed = [
            individuals_to_be_crossed[i: i+2]
            for i in range(0, len(individuals_to_be_crossed), 2)
        ]
        crossover_children = list(chain.from_iterable(
            self.config.crossover(individual_pair)
            for individual_pair in individual_pairs_to_be_crossed
        ))

        mutate_only_individuals = ordered_population[:mutate_only_count]
        new_individuals = [self.config.new_individuals_producer() for _ in range(new_individuals_count)]
        elitism_individuals = ordered_population[:elitism_count]

        individuals_to_be_mutated = crossover_children + mutate_only_individuals + new_individuals

        def mutate(individual: Individual) -> Individual:
            mutated_individual = reduce(
                lambda prev_individual, new_mutation: new_mutation(prev_individual),
                self.config.mutations,
                individual
            )
            return mutated_individual

        mutated_individuals = [
            mutate(individual)
            for individual in individuals_to_be_mutated
        ] if (self.config.mutations is not None) else individuals_to_be_mutated

        new_population = mutated_individuals + elitism_individuals

        print(f"Produced a new generation of size: {len(new_population)}. "
              f"Crossed: {len(crossover_children)}, new: {len(new_individuals)}, "
              f"elited: {len(elitism_individuals)}, only mutated: {len(mutate_only_individuals)}, "
              f"total mutated: {len(mutated_individuals)}")

        return new_population

    @staticmethod
    def _share2amount(total: int, share: float) -> int:
        return round(total * share)

    def serialize(self):
        config = {'crossoverShare': self.config.crossover_share,
                  'newIndividualsShare': self.config.new_individuals_share}
        if self.config.crossover:
            config['crossover'] = self.config.crossover.serialize()
        if self.config.mutations:
            config['mutations'] = [mutation.serialize()
                                   for mutation in self.config.mutations]
        return config
