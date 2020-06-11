import math
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import Callable, List, Optional, Tuple

from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, SubPopulation, \
    Individual
import numpy as np

Crossover = Callable[[SubPopulation], SubPopulation]
Mutation = Callable[[Individual], Individual]
IndividualProducer = Callable[[], Individual]


class FinsEvolver:

    @dataclass(frozen=True)
    class Config:
        use_crossover: bool = True
        use_mutation: bool = True
        elitism_count: int = 0

        crossover: Optional[Crossover] = None
        mutations: Optional[List[Mutation]] = None

    def __init__(self, config: Config):
        self.config = config

        if self.config.use_crossover and not config.crossover:
            raise ValueError("No crossover provided and should be used")

        if self.config.use_mutation and not config.mutations:
            raise ValueError("No mutations provided and should be used")

    def __call__(self, evaluated_population: EvaluatedPopulation) -> Population:

        feasible_evaluated_population = list(filter(
            lambda individual: individual['feasibility_score'] == 1.0,
            evaluated_population))

        infeasible_evaluated_population = list(filter(
            lambda individual: individual['feasibility_score'] != 1.0,
            evaluated_population))

        nan_population = [
            evaluated_individual
            for evaluated_individual in feasible_evaluated_population
            if math.isnan(evaluated_individual['novelty'])
        ]
        if len(nan_population) > 0:
            raise ValueError(f"nan feasible individuals: {nan_population}")

        new_feasible_population = self.evolve_population(
            feasible_evaluated_population,
            evaluation_attribute="novelty"
        )

        new_infeasible_population = self.evolve_population(
            infeasible_evaluated_population,
            evaluation_attribute="feasibility_score"
        )

        return new_feasible_population + new_infeasible_population

    def evolve_population(
            self,
            evaluated_population: EvaluatedPopulation,
            evaluation_attribute: str
    ) -> Population:
        population_count = len(evaluated_population)

        if self.config.elitism_count > 0:
            ordered_population = sorted(
                evaluated_population,
                key=lambda individual: individual[evaluation_attribute],
                reverse=True
            )
            elited_individuals = [
                evaluated_individual['individual']
                for evaluated_individual in ordered_population[:self.config.elitism_count]
            ]
            select_parents_evaluated_individuals = ordered_population[self.config.elitism_count:]
        else:
            elited_individuals = []
            select_parents_evaluated_individuals = evaluated_population

        if self.config.use_crossover and len(select_parents_evaluated_individuals) > 0:
            parents_count = len(select_parents_evaluated_individuals)
            parent_pairs = math.ceil(parents_count / 2)  # rounded up to produce an even number
            parent_pairs = self.proportionate_roulette_wheel_selection(
                select_parents_evaluated_individuals,
                evaluation_attribute,
                parent_pairs_count=parent_pairs,
                replacement=True
            )

            children = list(chain.from_iterable(
                self.config.crossover((parent1, parent2))
                for (parent1, parent2) in parent_pairs
            ))[:parents_count]  # removes the last child if there was not an even number of parents
        else:
            children = [
                evaluated_individual['individual']
                for evaluated_individual in select_parents_evaluated_individuals
            ]

        def mutate(individual: Individual) -> Individual:
            mutated_individual = reduce(
                lambda prev_individual, new_mutation: new_mutation(
                    prev_individual),
                self.config.mutations,
                individual
            )
            return mutated_individual

        mutated_children = [
            mutate(individual)
            for individual in children
        ] if self.config.use_mutation else children

        new_population = elited_individuals + mutated_children

        print(f"From a population of size: {population_count}. "
              f"Produced a new generation of size: {len(new_population)}. "
              f"elited: {len(elited_individuals)}")

        return new_population

    @staticmethod
    def _share2amount(total: int, share: float) -> int:
        return round(total * share)

    def serialize(self) -> Config:
        config = {'className': str(self.__class__), 'useCrossover': self.config.use_crossover,
                  'useMutation': self.config.use_mutation}
        if self.config.crossover:
            config['crossover'] = self.config.crossover.serialize()
        if self.config.mutations:
            config['mutations'] = [mutation.serialize()
                                   for mutation in self.config.mutations]
        return config

    @staticmethod
    def proportionate_roulette_wheel_selection(
            evaluated_population: EvaluatedPopulation,
            evaluation_attribute: str,
            parent_pairs_count: int,
            replacement: bool = True
    ) -> List[Tuple[Individual, Individual]]:
        """
        Chooses children of the same size as the given population
        """
        population_size = len(evaluated_population)

        parents_count = parent_pairs_count * 2

        evaluation_values = np.array([
            individual[evaluation_attribute]
            for individual in evaluated_population
        ])

        evaluation_values_sum = evaluation_values.sum()
        probabilities = evaluation_values / evaluation_values_sum if evaluation_values_sum != 0 \
            else np.ones(population_size) / population_size

        all_parents = np.random.choice(
            evaluated_population,
            size=parents_count,
            replace=replacement,
            p=probabilities
        )

        parent_pairs = [
            (all_parents[i]['individual'], all_parents[i+1]['individual'])
            for i in range(0, parents_count, 2)
        ]
        return parent_pairs
