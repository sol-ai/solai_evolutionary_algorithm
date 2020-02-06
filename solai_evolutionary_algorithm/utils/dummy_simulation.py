import random
import time

class DummySimulation:

    def evaluate_fitness(self, genome):
        time.sleep(10)
        return random.random()
