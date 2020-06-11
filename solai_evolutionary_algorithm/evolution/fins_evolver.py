import math
from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import Callable, List, Optional, Tuple

from solai_evolutionary_algorithm.evaluation.simulation.constrained_novelty_evaluation import InfeasibleObjective
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
        feasible_boost: bool = False
        infeasible_objective: InfeasibleObjective = InfeasibleObjective.FEASIBILITY

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

        feasible_boost = True
        if feasible_boost and 2 <= len(feasible_evaluated_population) < len(infeasible_evaluated_population):
            total_population_size = len(evaluated_population)
            new_feasible_population_size = math.floor(total_population_size / 2)
            new_infeasible_population_size = math.ceil(total_population_size / 2)
        else:
            new_feasible_population_size = len(feasible_evaluated_population)
            new_infeasible_population_size = len(infeasible_evaluated_population)

        new_feasible_population = self.evolve_population(
            feasible_evaluated_population,
            evaluation_attribute="novelty",
            new_population_size=new_feasible_population_size
        )

        new_infeasible_population = self.evolve_population(
            infeasible_evaluated_population,
            evaluation_attribute={
                InfeasibleObjective.FEASIBILITY: "feasibility_score",
                InfeasibleObjective.NOVELTY: "novelty"
            }[self.config.infeasible_objective],
            new_population_size=new_infeasible_population_size
        )

        return new_feasible_population + new_infeasible_population

    def evolve_population(
            self,
            evaluated_population: EvaluatedPopulation,
            evaluation_attribute: str,
            new_population_size: int
    ) -> Population:
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
            non_elited_evaluated_individuals = ordered_population[self.config.elitism_count:]
        else:
            elited_individuals = []
            non_elited_evaluated_individuals = evaluated_population

        children_count = new_population_size - len(elited_individuals)

        if self.config.use_crossover and len(evaluated_population) >= 2 and children_count > 0:
            parents_count = children_count
            parent_pairs_count = math.ceil(parents_count / 2)  # rounded up to produce an even number
            parent_pairs = self.proportionate_roulette_wheel_selection(
                evaluated_population,
                evaluation_attribute,
                parent_pairs_count=parent_pairs_count
            )

            children = list(chain.from_iterable(
                self.config.crossover((parent1, parent2))
                for (parent1, parent2) in parent_pairs
            ))[:parents_count]  # removes the last child if there was not an even number of parents
        else:
            children = [
                evaluated_individual['individual']
                for evaluated_individual in non_elited_evaluated_individuals
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

        print(f"From a population of size: {len(evaluated_population)}. "
              f"Produced a new generation of size: {len(new_population)}. "
              f"elited: {len(elited_individuals)}."
              f" Based on: {evaluation_attribute}")

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
            parent_pairs_count: int
    ) -> List[Tuple[Individual, Individual]]:
        """
        Chooses children of the same size as the given population
        """
        if len(evaluated_population) < 2:
            raise ValueError("A population of at least 2 is required for roulette wheel selection")

        population_size = len(evaluated_population)

        evaluation_values = np.array([
            individual[evaluation_attribute]
            for individual in evaluated_population
        ])

        evaluation_values_sum = evaluation_values.sum()
        probabilities = evaluation_values / evaluation_values_sum if evaluation_values_sum != 0 \
            else np.ones(population_size) / population_size

        evaluated_parent_pairs = [
            tuple(np.random.choice(
                evaluated_population,
                size=2,
                replace=False,
                p=probabilities
            ))
            for _ in range(parent_pairs_count)
        ]

        parent_pairs = [
            (evaluated_parent_pair[0]['individual'], evaluated_parent_pair[1]['individual'])
            for evaluated_parent_pair in evaluated_parent_pairs
        ]

        return parent_pairs
