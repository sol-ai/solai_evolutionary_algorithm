from dataclasses import dataclass, field
from functools import reduce
from typing import List

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

from solai_evolutionary_algorithm.evolution.evolution_types import Population, EvaluatedPopulation
from solai_evolutionary_algorithm.evolution.evolver_config import EvolverListener


@dataclass
class GenerationsData:
    populations_fitnesses: List[List[float]] = field(default_factory=list)
    populations_feasibility_score: List[List[float]] = field(default_factory=list)
    populations_novelty: List[List[float]] = field(default_factory=list)


def update_generations_data(generations_data: GenerationsData, evaluated_population: EvaluatedPopulation):
    generations_data.populations_fitnesses.append([
        sum(evaluated_individual['fitness'])
        for evaluated_individual in evaluated_population
    ])
    generations_data.populations_feasibility_score.append([
        evaluated_individual['feasibility_score']
        for evaluated_individual in evaluated_population
    ])
    generations_data.populations_novelty.append([
        evaluated_individual['novelty']
        for evaluated_individual in evaluated_population
    ])


class PlotGenerationsLocalService(EvolverListener):
    def __init__(self):
        self.feasible_generations_data = GenerationsData()
        self.infeasible_generations_data = GenerationsData()

        plt.ion()
        _, self.axes = plt.subplots(3, 2)
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.show()

    def on_start(self, *args):
        pass

    def on_new_generation(self, evaluated_population, is_last_generation) -> None:
        feasible_evaluated_population = [
            evaluated_individual
            for evaluated_individual in evaluated_population
            if evaluated_individual['feasibility_score'] == 1
        ]

        infeasible_evaluated_population = [
            evaluated_individual
            for evaluated_individual in evaluated_population
            if evaluated_individual['feasibility_score'] != 1
        ]

        update_generations_data(self.feasible_generations_data, feasible_evaluated_population)
        update_generations_data(self.infeasible_generations_data, infeasible_evaluated_population)

        feasible_pop_sizes = [
            len(pop)
            for pop in self.feasible_generations_data.populations_fitnesses
        ]

        infeasible_pop_sizes = [
            len(pop)
            for pop in self.infeasible_generations_data.populations_fitnesses
        ]

        # plt.figure(1)
        # # _, [ax1, ax2] = plt.subplots(1, 2)
        # plt.gcf().clear()
        for ax in self.axes.reshape(-1):
            ax.clear()

        feasible_novelty_ax = self.axes[0][0]
        feasible_feasibility_ax = self.axes[1][0]
        feasible_pop_size_ax = self.axes[2][0]

        infeasible_novelty_ax = self.axes[0][1]
        infeasible_feasibility_ax = self.axes[1][1]
        infeasible_pop_size_ax = self.axes[2][1]

        feasible_novelty_ax.boxplot(self.feasible_generations_data.populations_novelty)
        feasible_novelty_ax.set_title("feasible")
        feasible_novelty_ax.set_ylabel("novelty")

        feasible_feasibility_ax.boxplot(self.feasible_generations_data.populations_feasibility_score)
        feasible_feasibility_ax.set_ylabel("feasibility")

        feasible_pop_size_ax.plot(feasible_pop_sizes)
        feasible_pop_size_ax.set_ylabel("population size")
        feasible_pop_size_ax.set_xlabel("generations")

        infeasible_novelty_ax.boxplot(self.infeasible_generations_data.populations_novelty)
        infeasible_novelty_ax.set_title("infeasible")

        infeasible_feasibility_ax.boxplot(self.infeasible_generations_data.populations_feasibility_score)

        infeasible_pop_size_ax.plot(infeasible_pop_sizes)
        infeasible_pop_size_ax.set_xlabel("generations")

        plt.tight_layout()
        plt.draw()

        plt.pause(0.001)

    def on_end(self, *args, **kwargs):
        plt.ioff()
        plt.show()
