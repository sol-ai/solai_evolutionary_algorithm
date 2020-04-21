from solai_evolutionary_algorithm.socket.simulation_queue import SimulationQueue
from itertools import combinations
from copy import deepcopy
import sys


class Evaluation:

    character_id = None
    fitness = None
    novelty = None

    desired_game_length = 5000

    current_population_fitness = {}

    def __init__(self, simulation_queue):
        self.simulation_queue = simulation_queue

    def evaluate_one_population(self, population):

        current_simulations = []

        simulation_queue = self.simulation_queue

        for character in population:
            self.current_population_fitness[character['characterId']] = 0

        character_pairs = combinations(population, 2)

        for pair in character_pairs:
            simulation_id = simulation_queue.push_character_pair(*pair)
            simulation_dict = {'simulationId': simulation_id,
                               'characters': [pair[0]['characterId'], pair[1]['characterId']]}
            current_simulations.append(simulation_dict)

        simulation_result = simulation_queue.get_simulation_results()
        for i, simulation in enumerate(current_simulations):
            for result in simulation_result:
                if simulation['simulationId'] == result['simulationId']:
                    current_simulations[i]['result'] = result['metrics']
                    print(result['metrics'])

        self.evaluate_fitness(current_simulations)

        fitnesses = deepcopy(self.current_population_fitness)

        self.current_population_fitness = {}

        return fitnesses

    def evaluate_fitness(self, simulation_results):
        for result in simulation_results:
            character1_id = result['characters'][0]
            character2_id = result['characters'][1]

            metrics_result = result['result']

            for metric in metrics_result:
                if metric == 'gameWon':
                    if metrics_result[metric][0]:
                        self.current_population_fitness[character1_id] += 10
                    else:
                        self.current_population_fitness[character2_id] += 10
                if metric == 'gameLength':
                    game_length = metrics_result[metric][0]
                    difference = abs(self.desired_game_length - game_length)
                    normalized_difference = difference/1000
                    score = min(normalized_difference, 10)
                    self.current_population_fitness[character1_id] += 10 - score
                    self.current_population_fitness[character2_id] += 10 - score
