import unittest
from typing import List

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.initial_population_producers.from_existing_producers import FromExistingProducer


def char_equals_except_id(chars: List[CharacterConfig]):
    chars_without_id = [
        {**char, 'characterId': None}
        for char in chars
    ]
    return chars_without_id[1:] == chars_without_id[:-1]


def char_without_id(char: CharacterConfig):
    return {**char, 'characterId': None}


class FromExistingProducerTest(unittest.TestCase):

    def test_from_existing_producer(self):
        from_existing_producer = FromExistingProducer(
            population_size=10,
            chars_filename=[
                "shrankConfig.json",
                "schmathiasConfig.json",
                "brailConfig.json",
                "magnetConfig.json"
            ]
        )

        population = from_existing_producer()

        self.assertEqual(10, len(population), "Population size should be 10")
        self.assertEqual(population[0]['name'], "Shrank")
        self.assertEqual(population[1]['name'], "Schmathias")
        self.assertEqual(population[2]['name'], "Brail")
        self.assertEqual(population[3]['name'], "MagneT")

        self.assertEqual(char_without_id(population[0]), char_without_id(population[4]))
        self.assertEqual(char_without_id(population[0]), char_without_id(population[8]))

        self.assertEqual(char_without_id(population[1]), char_without_id(population[5]))
        self.assertEqual(char_without_id(population[1]), char_without_id(population[9]))

        self.assertEqual(char_without_id(population[2]), char_without_id(population[6]))

        self.assertEqual(char_without_id(population[3]), char_without_id(population[7]))
