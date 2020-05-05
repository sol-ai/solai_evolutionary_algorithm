from copy import deepcopy
from functools import reduce
from itertools import combinations, chain
from statistics import mean
from typing import List, Optional, Any, Dict, TypedDict, Iterable, cast, Tuple, OrderedDict

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import SimulationQueue, SimulationData, \
    CharacterConfig, SimulationResult
from solai_evolutionary_algorithm.evolution.evolution_types import Population, FitnessEvaluation, EvaluatedPopulation, \
    EvaluatedIndividual
from solai_evolutionary_algorithm.utils.kwargs_utils import filter_not_none_values


EvaluatedMetrics = Dict[str, List[float]]  # mapping metric name to a list of a value for each character

SimulationMeasurements = TypedDict("SimulationMeasurements", {
    'simulationId': str,
    'charactersId': List[str],  # character ids in the same order as measurements in EvaluatedMetrics
    'metrics': EvaluatedMetrics
})

CharacterAllMeasurements = Dict[str, List[float]]  # all measurements from a set of simulations by metric

CharactersAllMeasurements = Dict[str, CharacterAllMeasurements]  # CharacterAllMeasurements by characterId

MetricsByCharacter = Dict[str, Dict[str, float]]  # Each metric accumulated for each character



class SimulationFitnessEvaluation(FitnessEvaluation):
    character_id = None
    fitness = None
    novelty = None

    desired_values = {
        "leadChange": 50,
        "characterWon": 0.8,
        "stageCoverage": 0.7,
        "nearDeathFrames": 700,
        "gameLength": 7200
    }

    current_population_fitness = {}
    novel_archive = []

    def __init__(
            self,
            metrics: List[str],
            queue_host: Optional[str] = None,
            queue_port: Optional[int] = None
    ):
        self.simulation_queue = SimulationQueue(
            **filter_not_none_values({
                'host': queue_host,
                'port': queue_port
            })
        )
        self.metrics = metrics

    def __call__(self, population: Population) -> EvaluatedPopulation:
        return self.evaluate_one_population(population)

    def evaluate_one_population(self, population: Population) -> EvaluatedPopulation:

        character_simulations_count = len(population)-1  # assuming all pairs of characters are simulated

        simulations_results = self.simulate_population(population, self.simulation_queue)  # blocks until all finished

        # a simpler representation of results
        simulations_measurements = self.__simulation_results_to_simulation_measurements(simulations_results)

        # a list of all measurements for each metric for each character
        all_measurements_by_character: CharactersAllMeasurements =\
            self.__group_all_measures_by_character(simulations_measurements)

        metric_fitness_by_character = self.evaluate_fitness_all_characters(all_measurements_by_character)

        evaluated_population: EvaluatedPopulation = [
            EvaluatedIndividual(
                individual=individual,
                fitness=[metric_fitness_by_character[individual['characterId']]]
            )
            for individual in population
        ]

        return evaluated_population

    def simulate_population(
            self,
            population: Population,
            simulation_queue: SimulationQueue
    ) -> List[SimulationResult]:
        """
        Simulate combinations of characters and return simulation results
        """
        character_pairs: List[Tuple[CharacterConfig, CharacterConfig]] = combinations(population, 2)

        current_simulations_data = [
            SimulationData(
                simulationId=simulation_queue.create_simulation_id(),
                charactersConfigs=char_pair,
                metrics=self.metrics
            )
            for char_pair in character_pairs
        ]

        print(f"Pushing {len(current_simulations_data)} simulations, waiting for simulation results...\n\n")
        simulations_result = simulation_queue.push_simulations_data_wait_results(current_simulations_data)

        return simulations_result

    def evaluate_fitness_all_characters(
            self,
            characters_all_measurements: CharactersAllMeasurements
    ) -> Dict[str, float]:

        characters_metrics_score = self.__evaluate_characters_metrics_score(characters_all_measurements)

        # combine metrics scores for each character by accumulation
        def metrics_score_to_fitness(metrics_score: Dict[str, float]) -> float:
            return sum(metrics_score.values())

        fitness_by_character: Dict[str, float] = {
            char_id: metrics_score_to_fitness(char_metrics_score)
            for char_id, char_metrics_score in characters_metrics_score.items()
        }

        return fitness_by_character

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

    def __init_metric_values(self):
        return dict.fromkeys(self.desired_values, 0)

    def __evaluate_characters_metrics_score(
            self,
            characters_all_measurements: CharactersAllMeasurements
    ) -> Dict[str, Dict[str, float]]:
        # average all measurements for each character
        characters_averaged_measurements: Dict[str, Dict[str, float]] = {
            char_id: {
                metric: mean(measurements)
                for metric, measurements in char_metrics.items()
            }
            for char_id, char_metrics in characters_all_measurements.items()
        }

        # give a score to each metric for each character
        characters_metrics_score: Dict[str, Dict[str, float]] = {
            char_id: {
                metric: self.__evaluate_metric_score(metric, averaged_measurements)
                for metric, averaged_measurements in char_metrics.items()
            }
            for char_id, char_metrics in characters_averaged_measurements.items()
        }

        return characters_metrics_score

        # number_of_games_per_character = len(character_metrics_result) - 1
        # character_metrics_score = deepcopy(character_metrics_result)
        #
        # for char in character_metrics_score:
        #     for metric in character_metrics_score[char]:
        #         metric_score_per_game = character_metrics_score[char][metric] / \
        #                                 number_of_games_per_character
        #         character_metrics_score[char][metric] = self.__evaluate_metric_score(
        #             metric, metric_score_per_game)
        #
        # return character_metrics_score

    def __evaluate_metric_score(self, metric, average_metric_score):
        if metric not in self.desired_values:
            raise ValueError("Evaluating a metric with no desired value")

        if average_metric_score == 0:
            avg_score = 0.001
        else:
            avg_score = average_metric_score
        return 1 - min(abs(self.desired_values[metric] - avg_score) / self.desired_values[metric], 1)

    def __simulation_results_to_simulation_measurements(
            self,
            simulations_result: List[SimulationResult]
    ) -> List[SimulationMeasurements]:
        """
        map simulation results to SimulationMeasurements, a simpler representation
        """
        simulations_measurements: List[SimulationMeasurements] = cast(List[SimulationMeasurements], [
            SimulationMeasurements(
                simulationId=simulation_result['simulationId'],
                charactersId=[
                    character_config['characterId']
                    for character_config in simulation_result['simulationData']['charactersConfigs']
                ],
                metrics=simulation_result['metrics']
            )
            for simulation_result in simulations_result
        ])
        return simulations_measurements

    def __group_all_measures_by_character(
            self,
            simulations_measurements: List[SimulationMeasurements]
    ) -> CharactersAllMeasurements:
        """
        groups all measurements from all simulations by metric by character
        """
        def characters_measurements_reducer(
                prev_characters_measurements: CharactersAllMeasurements,
                simulation_measurements: SimulationMeasurements
        ) -> CharactersAllMeasurements:
            # will not copy the prev data as it is not necessary
            new_characters_measurements = prev_characters_measurements

            for i in range(2):  # allways two characters
                char_id: str = simulation_measurements['charactersId'][i]
                measurements: Dict[str, float] = {  # measurements for the given character
                    metric: measurement_by_char[i]
                    for metric, measurement_by_char in simulation_measurements['metrics'].items()
                }
                if char_id not in new_characters_measurements:
                    # use the measurements as initial value for the character. Measurements are converted to a list
                    new_characters_measurements[char_id] = {
                        metric: [measurement]
                        for metric, measurement in measurements.items()
                    }
                else:
                    # if measurements already provided for the given character, append new measurements
                    for metric, measurement in measurements.items():
                        new_characters_measurements[char_id][metric].append(measurement)

            return new_characters_measurements

        all_measurements_by_character = reduce(
            characters_measurements_reducer,
            simulations_measurements,
            {}  # start with an empty object
        )

        return all_measurements_by_character

    # def __count_simulations_per_character(
    #         self,
    #         simulated_characters_ids: List[str],
    #         simulations_results: List[SimulationMeasurements]
    # ) -> Dict[str, int]:
    #     def characters_simulations_count_reducer(
    #             _simulations_count_per_character: Dict[str, int],
    #             simulation_measurements: SimulationMeasurements
    #     ) -> Dict[str, int]:
    #         for i in range(2):
    #             char_id = simulation_measurements['charactersId'][i]
    #             _simulations_count_per_character[char_id] += 1
    #         return _simulations_count_per_character
    #
    #     simulations_count_per_character = reduce(
    #         characters_simulations_count_reducer,
    #         simulations_results,
    #         initial={char_id: 0 for char_id in simulated_characters_ids}
    #     )
    #
    #     return simulations_count_per_character


        # def __accumulate_metrics_for_each_character(
        #         self,
        #         simulations_measurements: List[SimulationMeasurements]
        # ) -> MetricsByCharacter:
        #     """
        #     Accumulates metric evaluations for each character
        #     assuming each simulation measures the same metrics (or else this will fail)
        #     """
        # characters_accumulated_measurements = {}
        #
        # for simulation_measurements in cast(List[SimulationMeasurements], simulations_measurements):
        #     for char_index in range(2):  # two characters for each simulation result
        #         char_id = simulation_measurements['charactersId'][char_index]
        #         char_measurements = {}
        #         for metric, measurements in simulation_measurements['metrics'].items():
        #             char_measurements[metric] = measurements[char_index]
        #
        #         if char_id not in characters_accumulated_measurements:
        #             characters_accumulated_measurements[char_id] = char_measurements
        #         else:
        #             for metric, measurement in char_measurements.items():
        #                 characters_accumulated_measurements[char_id][metric] += measurement
        #
        # return characters_accumulated_measurements