import json
from typing import List, cast

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolution.evolution_types import InitialPopulationProducer, Population
from pkg_resources import resource_stream


class FromExistingProducer(InitialPopulationProducer):
    """
    Generates a population from existing characters, applying mutations / crossovers
    """

    def __init__(self, population_size: int, chars_filename: List[str]):
        self.population_size = population_size
        self.chars_filename = chars_filename

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
        def load_char(filename: str) -> CharacterConfig:
            char_file = resource_stream('solai_evolutionary_algorithm', f"resources/existing_characters/{filename}")
            char_config = json.load(char_file)
            char_file.close()
            return char_config

        existing_chars = cast(List[CharacterConfig], [
            load_char(char_filename)
            for char_filename in self.chars_filename
        ])

        population = self.__duplicate_chars_to_size(existing_chars, self.population_size)
        return population
