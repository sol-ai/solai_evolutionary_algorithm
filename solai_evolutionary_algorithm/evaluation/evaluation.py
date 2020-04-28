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
    novel_archive = []

    def __init__(self, simulation_queue):
        self.simulation_queue = simulation_queue

    def evaluate_one_population(self, population):

        current_simulations = []

        simulation_queue = self.simulation_queue

        for character in population:
            self.current_population_fitness[character['characterId']] = 0

        character_pairs = combinations(population, 2)

        print("pushing simulations...\n\n")
        for pair in character_pairs:
            simulation_id = simulation_queue.push_character_pair(*pair)
            simulation_dict = {'simulationId': simulation_id,
                               'characters': [pair[0]['characterId'], pair[1]['characterId']]}
            current_simulations.append(simulation_dict)

        print("waiting for simulation results...\n\n")
        simulation_result = simulation_queue.get_simulation_results()
        for i, simulation in enumerate(current_simulations):
            for result in simulation_result:
                if simulation['simulationId'] == result['simulationId']:
                    current_simulations[i]['result'] = result['metrics']

        self.evaluate_fitness(current_simulations)

        fitnesses = deepcopy(self.current_population_fitness)

        self.current_population_fitness = {}

        return fitnesses

    def evaluate_fitness(self, simulation_data):
        for sim_data in simulation_data:
            character1_id = sim_data['characters'][0]
            character2_id = sim_data['characters'][1]

            metrics_result = sim_data['result']

            for metric in metrics_result:
                if metric == 'characterWon':
                    if metrics_result[metric][0]:
                        self.current_population_fitness[character1_id] += 10
                    else:
                        self.current_population_fitness[character2_id] += 10
                if metric == 'gameLength':
                    game_length = metrics_result[metric][0]
                    difference = abs(self.desired_game_length - game_length)
                    normalized_difference = difference/1000
                    game_length_score = min(normalized_difference, 100)
                    self.current_population_fitness[character1_id] += (
                        100 - game_length_score)
                    self.current_population_fitness[character2_id] += (
                        100 - game_length_score)

                    near_death_frames_character1 = metrics_result['nearDeathFrames'][0]
                    near_death_frames_character2 = metrics_result['nearDeathFrames'][1]

                    near_death_score1 = 100 * \
                        (near_death_frames_character1/game_length)
                    near_death_score2 = 100 * \
                        (near_death_frames_character2/game_length)

                    self.current_population_fitness[character1_id] += near_death_score1
                    self.current_population_fitness[character2_id] += near_death_score2

    def evaluate_metric_score(self, metric):
        pass
