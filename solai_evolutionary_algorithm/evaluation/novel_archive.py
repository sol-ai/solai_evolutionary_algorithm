import sys
from dataclasses import dataclass
from statistics import mean
from typing import Dict, Tuple, Any, Optional, List
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, Population, Individual, EvaluatedPopulation
from solai_evolutionary_algorithm.utils.character_distance_utils import normalized_euclidean_distance


class NovelArchive:

    @dataclass(frozen=True)
    class Config:
        novel_archive_size: int
        nearest_neighbour_number: int

        character_properties_ranges: Dict[str, Tuple[Any, Any]]
        melee_ability_ranges: Dict[str, Tuple[Any, Any]]
        projectile_ability_ranges: Dict[str, Tuple[Any, Any]]

    novel_archive = []

    def __init__(self, config):
        self.config = config

    def __len__(self):
        return len(self.novel_archive)

    def get_all_individuals(self) -> List[Individual]:
        return self.novel_archive

    def calculate_novelty_of_population(self, population: EvaluatedPopulation) -> None:
        distances_to_population = {individual['individual']['characterId']:
                                   sorted(
                                   [self.__normalized_euclidean_distance(individual['individual'], other_individual['individual'])
                                    for other_individual in population
                                    if other_individual['individual']['characterId'] != individual['individual']['characterId']]
                                   )
                                   for individual in population
                                   }
        for individual in population:
            individual['populationNovelty'] = mean(distances_to_population[individual['individual']
                                                                           ['characterId']][:self.config.nearest_neighbour_number])

    def calculate_archive_novelty(self, population: EvaluatedPopulation) -> None:
        for individual in population:
            individual['archiveNovelty'] = self.__calculate_novelty_compared_to_archive(
                individual)

    def consider_population_for_archive(self, population) -> None:
        if (self.config.novel_archive_size - len(self.novel_archive)) >= len(population):
            self.novel_archive.extend(population)
        elif (self.config.novel_archive_size - len(self.novel_archive)) > 0:
            remaining = self.config.novel_archive_size - \
                len(self.novel_archive)
            sorted_population = sorted(
                population, key=lambda individual: individual['populationNovelty'], reverse=True)
            self.novel_archive.extend(sorted_population[:remaining])
        else:
            for individual in population:
                self.replace_if_more_novel_than_least_novel_in_archive(
                    individual)
        self.__update_novelty_in_archive()

    def replace_if_more_novel_than_least_novel_in_archive(self, individual) -> None:
        sorted_archive = sorted(
            self.novel_archive,
            key=lambda individual: individual['archiveNovelty'],
            reverse=True)

        if individual['archiveNovelty'] > sorted_archive[-1]['archiveNovelty']:
            sorted_archive[-1] = individual
            self.novel_archive = sorted_archive

    def __update_novelty_in_archive(self) -> None:

        def reset_novelty(individual):
            individual['archiveNovelty'] = 0
            return individual

        self.novel_archive = list(
            map(lambda individual: reset_novelty(individual), self.novel_archive))

        for individual in self.novel_archive:
            individual['novelty'] = self.__calculate_novelty_compared_to_archive(
                individual)

    def __calculate_novelty_compared_to_archive(self, individual: Individual) -> float:
        distances_to_individuals = {}
        for archive_individual in self.novel_archive:
            arch_ind_id = archive_individual['individual']['characterId']
            distances_to_individuals[arch_ind_id] = self.__normalized_euclidean_distance(
                individual['individual'], archive_individual['individual'])

        individual_character_id = individual['individual']['characterId']
        if individual_character_id in distances_to_individuals:
            del distances_to_individuals[individual_character_id]

        ordered_distances = sorted(
            distances_to_individuals.values())

        novelty = sum(
            ordered_distances[:self.config.nearest_neighbour_number])/self.config.nearest_neighbour_number
        return novelty

    def __normalized_euclidean_distance(self, individual1: Individual, individual2: Individual) -> float:
        return normalized_euclidean_distance(individual1, individual2, self.config.character_properties_ranges, self.config.melee_ability_ranges, self.config.projectile_ability_ranges)
