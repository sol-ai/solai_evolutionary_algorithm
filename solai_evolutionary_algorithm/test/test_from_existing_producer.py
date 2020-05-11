import unittest

from solai_evolutionary_algorithm.initial_population_producers.from_existing_producers import FromExistingProducer


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

        self.assertEqual(3, population.count(population[0]), "Should be 3 of the first char")
        self.assertEqual(3, population.count(population[1]), "Should be 3 of the second char")
        self.assertEqual(2, population.count(population[2]), "Should be 2 of the third char")
        self.assertEqual(2, population.count(population[3]), "Should be 2 of the fourth char")
