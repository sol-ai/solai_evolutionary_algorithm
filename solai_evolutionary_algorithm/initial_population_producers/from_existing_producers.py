import json
from typing import List, cast, Dict, Optional

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, Population
from pkg_resources import resource_stream

from solai_evolutionary_algorithm.evolution.generation_evolver import Mutation
from solai_evolutionary_algorithm.utils.character_id import create_character_id


def load_char_from_file(filename: str) -> CharacterConfig:
    char_file = resource_stream(
        'solai_evolutionary_algorithm', f"resources/{filename}")
    char_config = json.load(char_file)
    char_file.close()
    return char_config


class FromExistingProducer(InitialPopulationProducer):
    """
    Generates a population from existing characters, applying mutations / crossovers
    """

    def __init__(self, population_size: int, chars_filename: List[str], mutation: Optional[Mutation] = None):
        self.population_size = population_size
        self.chars_filename = chars_filename
        self.mutation = mutation

    @staticmethod
    def __duplicate_chars_to_size(chars: List[CharacterConfig], size: int) -> List[CharacterConfig]:
        existing_chars_count = len(chars)
        duplication_count = size-existing_chars_count
        duplicated_chars = [
            chars[i % existing_chars_count]
            for i in range(duplication_count)
        ]
        return chars + duplicated_chars

    def __call__(self) -> Population:
        existing_chars_without_id = cast(List[CharacterConfig], [
            load_char_from_file(f"existing_characters/{char_filename}")
            for char_filename in self.chars_filename
        ])

        population_without_id = self.__duplicate_chars_to_size(
            existing_chars_without_id, self.population_size)
        population = [
            {
                **char_without_id,
                'characterId': create_character_id()
            }
            for char_without_id in population_without_id
        ]

        if self.mutation is not None:
            keep_char_count = len(self.chars_filename)
            individuals_to_be_mutated = population[keep_char_count:]
            individuals_to_be_kept = population[:keep_char_count]
            mutated_population = [
                self.mutation(char)
                for char in individuals_to_be_mutated
            ]
            initial_population = individuals_to_be_kept + mutated_population
        else:
            initial_population = population

        return initial_population

    def serialize(self) -> Dict:
        return {'description': "From existing characters producer", 'populationSize': self.population_size, 'characterFileName': self.chars_filename}
