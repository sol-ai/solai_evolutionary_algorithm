from dataclasses import dataclass
from typing import Dict, Tuple, Any, Optional, List
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, Population, Individual
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

    def consider_individual_for_archive(self, individual: Individual) -> None:
        if len(self.novel_archive) < self.config.novel_archive_size:
            self.novel_archive.append(individual)
        elif self.__is_more_novel_than_least_novel_in_archive(individual):
            sorted_novel_archive = sorted(
                self.novel_archive, key=lambda individual: individual['novelty'], reverse=True)
            sorted_novel_archive[-1] = individual
            self.novel_archive = sorted_novel_archive

        self.__update_novelty_in_archive()

    def __is_more_novel_than_least_novel_in_archive(self, individual: Individual) -> bool:
        ordered_novel_archive = sorted(
            self.novel_archive, key=lambda individual: individual['novelty'], reverse=True)
        return self.__calculate_novelty_compared_to_archive(individual) > ordered_novel_archive[-1]['novelty']

    def __update_novelty_in_archive(self) -> None:

        def reset_novelty(individual):
            individual['novelty'] = 0
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
