
import math
import numbers
from dataclasses import dataclass
from functools import reduce
from itertools import chain, combinations
from typing import Callable, List, Optional, Tuple, Dict, Any
from solai_evolutionary_algorithm.utils.character_distance_utils import normalized_euclidean_distance

from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, SubPopulation, \
    Individual, EvaluatedIndividual, NoveltyAndFitnessEvaluatedPopulation, NoveltyAndFitnessEvaluatedIndividual

Crossover = Callable[[SubPopulation], SubPopulation]
Mutation = Callable[[Individual], Individual]
IndividualProducer = Callable[[], Individual]


class FitnessAndNoveltyEvolver:
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
        novel_archive_size: int
        character_properties_ranges: Dict[str, Tuple[Any, Any]]
        melee_ability_ranges: Dict[str, Tuple[Any, Any]]
        projectile_ability_ranges: Dict[str, Tuple[Any, Any]]
        crossover: Optional[Crossover] = None
        mutations: Optional[List[Mutation]] = None
        new_individuals_producer: Optional[IndividualProducer] = None

    novel_archive = []

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

        novelty_evaluated_population = self.evaluate_novelty(
            evaluated_population)

        self.consider_for_novel_archive(novelty_evaluated_population)

        ordered_evaluated_population = sorted(
            evaluated_population,
            key=fitness_retriever,
            reverse=True
        )

        fitness_threshold = int(len(ordered_evaluated_population)/2)

        novelty_evaluated_population = self.evaluate_novelty(
            ordered_evaluated_population[:fitness_threshold])

        self.consider_for_novel_archive(novelty_evaluated_population)
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

    def __euclidean_distance(self, individual1, individual2):
        return

    def evaluate_novelty(self, evaluated_population: EvaluatedPopulation) -> NoveltyAndFitnessEvaluatedPopulation:
        config = self.config
        novelty_and_fitness_evaluated_population = evaluated_population
        individual_pairs = combinations(
            novelty_and_fitness_evaluated_population, 2)
        for pair in individual_pairs:
            if 'populationNovelty' not in pair[0]:
                pair[0]['populationNovelty'] = 0
            if 'populationNovelty' not in pair[1]:
                pair[1]['populationNovelty'] = 0
            character_distance = normalized_euclidean_distance(pair[0]['individual'], pair[1]['individual'], config.character_properties_ranges,
                                                               config.melee_ability_ranges, config.projectile_ability_ranges)
            pair[0]['populationNovelty'] += character_distance / \
                len(evaluated_population)
            pair[1]['populationNovelty'] += character_distance / \
                len(evaluated_population)

        return novelty_and_fitness_evaluated_population

    def consider_for_novel_archive(self, novelty_and_fitness_evaluated_population: NoveltyAndFitnessEvaluatedPopulation) -> None:
        ordered_novelty_and_fitness_evaluated_population = sorted(
            novelty_and_fitness_evaluated_population, key=lambda individual: individual['populationNovelty'], reverse=True)
        if not self.novel_archive:
            self.novel_archive.extend(
                ordered_novelty_and_fitness_evaluated_population[:self.config.novel_archive_size])
        elif len(self.novel_archive) < self.config.novel_archive_size:
            remaining = self.config.novel_archive_size - \
                len(self.novel_archive)
            self.novel_archive.extend(
                ordered_novelty_and_fitness_evaluated_population[:remaining]
            )
        else:
            for individual in ordered_novelty_and_fitness_evaluated_population:
                self.consider_individual_for_novel_archive(individual)

        self.update_novelty_in_archive()

    def consider_individual_for_novel_archive(self, individual) -> None:
        if self.is_more_novel_than_least_novel_in_archive(individual):
            self.novel_archive = sorted(
                self.novel_archive, key=lambda individual: individual['archiveNovelty'])
            self.novel_archive[-1] = individual

    def is_more_novel_than_least_novel_in_archive(self, individual) -> bool:
        ordered_novel_archive = sorted(
            self.novel_archive, key=lambda individual: individual['archiveNovelty'])
        individual['archiveNovelty'] = 0
        for other_individual in ordered_novel_archive[:-1]:
            individual['archiveNovelty'] += normalized_euclidean_distance(
                individual['individual'], other_individual['individual'], self.config.character_properties_ranges, self.config.melee_ability_ranges, self.config.projectile_ability_ranges)
        return individual['archiveNovelty'] > ordered_novel_archive[-1]['archiveNovelty']

    def update_novelty_in_archive(self) -> None:
        config = self.config

        def reset_novelty(individual):
            individual['archiveNovelty'] = 0
            return individual

        self.novel_archive = list(
            map(lambda individual: reset_novelty(individual), self.novel_archive))
        novel_archive_pairs = combinations(
            self.novel_archive, 2)
        for pair in novel_archive_pairs:
            if 'archiveNovelty' not in pair[0]:
                pair[0]['archiveNovelty'] = 0
            if 'archiveNovelty' not in pair[1]:
                pair[1]['archiveNovelty'] = 0
            character_distance = normalized_euclidean_distance(pair[0]['individual'], pair[1]['individual'], config.character_properties_ranges,
                                                               config.melee_ability_ranges, config.projectile_ability_ranges)
            pair[0]['archiveNovelty'] += character_distance / \
                len(self.novel_archive)
            pair[1]['archiveNovelty'] += character_distance / \
                len(self.novel_archive)

    @staticmethod
    def _share2amount(total: int, shares: List[float]) -> List[int]:
        return [
            round(total * x)
            for x in shares
        ]

    def get_ordered_novel_archive(self):
        return sorted(self.novel_archive, key=lambda individual: individual['archiveNovelty'], reverse=True)

    def get_novel_archive_values(self):
        return list(map(lambda individual: individual['archiveNovelty'], self.novel_archive))

    def serialize(self) -> Config:
        config = {'crossoverShare': self.config.crossover_share,
                  'newIndividualsShare': self.config.new_individuals_share, 'novelArchiveSize': self.config.novel_archive_size}
        if self.config.crossover:
            config['crossover'] = self.config.crossover.serialize()
        if self.config.mutations:
            config['mutations'] = [mutation.serialize()
                                   for mutation in self.config.mutations]
        return config
