from functools import reduce

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

from solai_evolutionary_algorithm.evolution.evolver_config import EvolverListener


class PlotGenerationsLocalService(EvolverListener):

    def __init__(self):
        self.populations_fitness = []

        plt.ion()
        plt.figure(1)
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.show()

    def on_start(self, *args):
        pass

    def on_new_generation(self, evaluated_population, is_last_generation) -> None:
        self.populations_fitness.append([
            sum(evaluated_individual['fitness'])
            for evaluated_individual in evaluated_population
        ])

        plt.figure(1)
        plt.gcf().clear()
        plt.boxplot(self.populations_fitness)
        plt.draw()

        plt.pause(0.001)

    def on_end(self, *args, **kwargs):
        pass
