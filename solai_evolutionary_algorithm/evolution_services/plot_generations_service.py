from functools import reduce

from matplotlib.figure import Figure

from solai_evolutionary_algorithm.evolution.evolver import EvolutionListener
import matplotlib.pyplot as plt


class PlotGenerationsLocalService(EvolutionListener):

    def __init__(self):
        self.populations_fitness = []

        plt.ion()
        plt.figure(1)
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.show()

    def __call__(self, population, evaluated_population, is_last_generation) -> None:
        self.populations_fitness.append([
            sum(evaluated_individual['fitness'])
            for evaluated_individual in evaluated_population
        ])
        print(f"populations fitnesses: {self.populations_fitness}")
        plt.figure(1)
        plt.gcf().clear()
        plt.boxplot(self.populations_fitness)
        plt.draw()

        if not is_last_generation:
            plt.pause(0.001)
        else:
            plt.ioff()
            plt.show()

    def on_new_generation(self, evaluated_population, is_last_generation):

        self.populations_fitness.append([
            sum(evaluated_individual['fitness'])
            for evaluated_individual in evaluated_population
        ])
        print(f"populations fitnesses: {self.populations_fitness}")
        plt.figure(1)
        plt.gcf().clear()
        plt.boxplot(self.populations_fitness)
        plt.draw()

        if not is_last_generation:
            plt.pause(0.001)
        else:
            plt.ioff()
            plt.show()
