import math
import numbers
from dataclasses import dataclass
from functools import reduce
from itertools import chain, combinations
from typing import Callable, List, Optional, Tuple, Dict, Any
from solai_evolutionary_algorithm.utils.character_distance_utils import normalized_euclidean_distance
from solai_evolutionary_algorithm.evaluation.novel_archive import NovelArchive
from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, SubPopulation, \
    Individual, EvaluatedIndividual, NoveltyAndFitnessEvaluatedPopulation, NoveltyAndFitnessEvaluatedIndividual

Crossover = Callable[[SubPopulation], SubPopulation]
Mutation = Callable[[Individual], Individual]
IndividualProducer = Callable[[], Individual]


class NoveltyAndFitnessEvolver:

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

        novel_archive: NovelArchive

        character_properties_ranges: Dict[str, Tuple[Any, Any]]
        melee_ability_ranges: Dict[str, Tuple[Any, Any]]
        projectile_ability_ranges: Dict[str, Tuple[Any, Any]]

        crossover: Optional[Crossover] = None
        mutations: Optional[List[Mutation]] = None
        new_individuals_producer: Optional[IndividualProducer] = None

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

        fitness_threshold = max(
            int(len(ordered_evaluated_population)/2), 2)

        self.consider_for_novel_archive(
            ordered_evaluated_population[:fitness_threshold])

        ordered_population = [
            evaluated_individual['individual']
            for evaluated_individual in ordered_evaluated_population
        ]

        population_count = len(ordered_evaluated_population)

        raw_crossover_count = self._share2amount(
            population_count, self.config.crossover_share)
        if raw_crossover_count % 2 != 0:
            print(
                f"Crossover count rounded down to be even, from: {raw_crossover_count}")
            crossover_count = raw_crossover_count - 1
        else:
            crossover_count = raw_crossover_count

        mutate_only_count = self._share2amount(
            population_count, self.config.mutate_only_share)
        new_individuals_count = self._share2amount(
            population_count, self.config.new_individuals_share)
        elitism_count = self._share2amount(
            population_count, self.config.elitism_share)

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
        new_individuals = [self.config.new_individuals_producer()
                           for _ in range(new_individuals_count)]
        elitism_individuals = ordered_population[:elitism_count]

        individuals_to_be_mutated = crossover_children + \
            mutate_only_individuals + new_individuals

        def mutate(individual: Individual) -> Individual:
            mutated_individual = reduce(
                lambda prev_individual, new_mutation: new_mutation(
                    prev_individual),
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

    def normalized_euclidean_distance(self, individual1, individual2):
        return normalized_euclidean_distance(individual1, individual2, self.config.character_properties_ranges, self.config.melee_ability_ranges, self.config.projectile_ability_ranges)

    # def evaluate_novelty_within_population(self, evaluated_population: EvaluatedPopulation) -> NoveltyAndFitnessEvaluatedPopulation:
    #     novelty_and_fitness_evaluated_population = evaluated_population
    #     individual_pairs = combinations(
    #         novelty_and_fitness_evaluated_population, 2)
    #     for pair in individual_pairs:
    #         if 'novelty' not in pair[0]:
    #             pair[0]['novelty'] = 0
    #         if 'novelty' not in pair[1]:
    #             pair[1]['novelty'] = 0
    #         character_distance = self.normalized_euclidean_distance(
    #             pair[0]['individual'], pair[1]['individual'])
    #         pair[0]['novelty'] += character_distance / \
    #             len(evaluated_population)
    #         pair[1]['novelty'] += character_distance / \
    #             len(evaluated_population)

    #     return novelty_and_fitness_evaluated_population

    def consider_for_novel_archive(self, evaluated_population: EvaluatedPopulation) -> None:
        for individual in evaluated_population:
            self.config.novel_archive.consider_individual_for_archive(
                individual)

    @staticmethod
    def _share2amount(total: int, share: float) -> int:
        return round(total * share)

    def get_ordered_novel_archive(self):
        return sorted(self.config.novel_archive.get_all_individuals(), key=lambda individual: individual['novelty'], reverse=True)

    def get_novel_archive_values(self) -> List:
        return list(map(lambda individual: individual['novelty'], self.config.novel_archive.get_all_individuals()))

    def serialize(self) -> Config:
        config = {'crossoverShare': self.config.crossover_share,
                  'newIndividualsShare': self.config.new_individuals_share, 'novelArchiveSize': len(self.config.novel_archive)}
        if self.config.crossover:
            config['crossover'] = self.config.crossover.serialize()
        if self.config.mutations:
            config['mutations'] = [mutation.serialize()
                                   for mutation in self.config.mutations]
        return config
