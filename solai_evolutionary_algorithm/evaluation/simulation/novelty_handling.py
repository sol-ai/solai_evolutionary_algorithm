from statistics import mean
from typing import List, Callable, Dict, Tuple

from solai_evolutionary_algorithm.evolution.evolution_types import Population, Individual

IndividualsWithDistance = List[Tuple[Individual, float]]
NovelArchive = List[Individual]


def average_distance_of_closest(
        individual: Individual,
        compare_to_individuals: List[Individual],
        consider_count: int,
        distance_func: Callable[[Individual, Individual], float]
) -> float:
    distances = [
        distance_func(individual, other_individual)
        for other_individual in compare_to_individuals
    ]
    distances_ordered = sorted(distances)
    considered_distances = distances_ordered[:consider_count]
    return mean(considered_distances)


def calculate_distance_and_update_novel_archive(
        population: Population,
        novel_archive: NovelArchive,
        distance_func: Callable[[Individual, Individual], float],
        distance_consider_count: int,
        insert_most_novel_count: int
) -> Tuple[IndividualsWithDistance, NovelArchive]:
    """
    Calculates the average distance from each individual in the given population
    to the distance_consider_count closest individuals from the given population and the novel archive.

    Returns each individual with the average distance calculated in descending order
    and an updated novel_archive with the insert_most_novel_count most novel in the population added.
    """

    compare_to_individuals = novel_archive + population

    average_distance_by_character: List[Tuple[Individual, float]] = [
        (individual, average_distance_of_closest(
            individual,
            compare_to_individuals,
            consider_count=distance_consider_count,
            distance_func=distance_func
        ))
        for individual in population
    ]

    average_distance_by_character_ordered: List[Tuple[Individual, float]] = sorted(
        average_distance_by_character,
        key=lambda item: item[1],
        reverse=True
    )

    insert_into_novel_archive = [
        character_with_average_distance[0]
        for character_with_average_distance in average_distance_by_character_ordered[:insert_most_novel_count]
    ]

    updated_novel_archive = novel_archive + insert_into_novel_archive

    return average_distance_by_character_ordered, updated_novel_archive



