from itertools import combinations
from copy import deepcopy


class Evaluation:

    character_id = None
    fitness = None
    novelty = None

    desired_values = {"leadChange": 50, "characterWon": 0.8,
                      "stageCoverage": 0.7, "nearDeathFrames": 700, "gameLength": 7200}

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
        character_metrics_result = self.__sort_accumulated_metrics_on_character(
            simulation_data)

        character_metrics_score = self.__evaluate_character_metrics_score(
            character_metrics_result)

        for character in character_metrics_score:
            for score in character_metrics_score[character]:
                self.current_population_fitness[character] += character_metrics_score[character][score]

        # for sim_data in simulation_data:
        #     character1_id = sim_data['characters'][0]
        #     character2_id = sim_data['characters'][1]

        #     metrics_result = sim_data['result']

        #     for metric in metrics_result:
        #         if metric == 'characterWon':
        #             if metrics_result[metric][0]:
        #                 self.current_population_fitness[character1_id] += 10
        #             else:
        #                 self.current_population_fitness[character2_id] += 10
        #         if metric == 'gameLength':
        #             game_length = metrics_result[metric][0]
        #             difference = abs(
        #                 self.desired_values['gameLength'] - game_length)
        #             normalized_difference = difference/1000
        #             game_length_score = min(normalized_difference, 100)
        #             self.current_population_fitness[character1_id] += (
        #                 100 - game_length_score)
        #             self.current_population_fitness[character2_id] += (
        #                 100 - game_length_score)

        #             near_death_frames_character1 = metrics_result['nearDeathFrames'][0]
        #             near_death_frames_character2 = metrics_result['nearDeathFrames'][1]

        #             near_death_score1 = 100 * \
        #                 (near_death_frames_character1/game_length)
        #             near_death_score2 = 100 * \
        #                 (near_death_frames_character2/game_length)

        #             self.current_population_fitness[character1_id] += near_death_score1
        #             self.current_population_fitness[character2_id] += near_death_score2

    def __sort_accumulated_metrics_on_character(self, simulation_data):
        character_metric_score = {}

        for simulation in simulation_data:

            char1_id = simulation['characters'][0]
            char2_id = simulation['characters'][1]
            if not char1_id in character_metric_score:
                character_metric_score[char1_id] = self.__init_metric_values()
            if not char2_id in character_metric_score:
                character_metric_score[char2_id] = self.__init_metric_values()

            result = simulation['result']
            for metric in result:
                character_metric_score[char1_id][metric] += result[metric][0]
                character_metric_score[char2_id][metric] += result[metric][1]

        return character_metric_score

    def __init_metric_values(self):
        return dict.fromkeys(self.desired_values, 0)

    def __evaluate_character_metrics_score(self, character_metrics_result):
        number_of_games_per_character = len(character_metrics_result) - 1
        character_metrics_score = deepcopy(character_metrics_result)

        for char in character_metrics_score:
            for metric in character_metrics_score[char]:
                metric_score_per_game = character_metrics_score[char][metric] / \
                    number_of_games_per_character
                character_metrics_score[char][metric] = self.__evaluate_metric_score(
                    metric, metric_score_per_game)

        return character_metrics_score

    def __evaluate_metric_score(self, metric, average_metric_score):
        if average_metric_score == 0:
            avg_score = 0.001
        else:
            avg_score = average_metric_score
        return 1-min(abs(self.desired_values[metric] - avg_score)/self.desired_values[metric], 1)
