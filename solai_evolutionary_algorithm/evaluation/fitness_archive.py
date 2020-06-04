from dataclasses import dataclass
from typing import Dict, Tuple, Any, Optional, List
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, Population, Individual


class FitnessArchive:

    @dataclass(frozen=True)
    class Config:
        fitness_archive_size: int

    fitness_archive = []

    def __init__(self, config):
        self.config = config

    def __len__(self):
        return len(self.fitness_archive)

    def get_all_individuals(self) -> List[Individual]:
        return self.fitness_archive

    def consider_individual_for_archive(self, individual: Individual) -> None:
        if len(self.fitness_archive) < self.config.fitness_archive_size:
            self.fitness_archive.append(individual)
        elif self.__is_fitter_than_least_fit_in_archive(individual):
            sorted_fitness_archive = sorted(
                self.fitness_archive, key=lambda individual: individual['fitness'], reverse=True)
            sorted_fitness_archive[-1] = individual
            self.fitness_archive = sorted_fitness_archive

    def __is_fitter_than_least_fit_in_archive(self, individual: Individual) -> bool:
        return min(map(lambda individual: individual['fitness'], self.fitness_archive)) < individual['fitness']
