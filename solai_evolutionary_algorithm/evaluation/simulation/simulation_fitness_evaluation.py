from copy import deepcopy
from functools import reduce
from itertools import combinations, chain
from statistics import mean
from typing import List, Optional, Any, Dict, TypedDict, Iterable, cast, Tuple, OrderedDict
from abc import ABC

from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import SimulationQueue, SimulationData, \
    CharacterConfig, SimulationResult
from solai_evolutionary_algorithm.evolution.evolution_types import Population, FitnessEvaluation, EvaluatedPopulation, \
    EvaluatedIndividual
from solai_evolutionary_algorithm.utils.kwargs_utils import filter_not_none_values


# mapping metric name to a list of a value for each character
EvaluatedMetrics = Dict[str, List[float]]

SimulationMeasurements = TypedDict("SimulationMeasurements", {
    'simulationId': str,
    # character ids in the same order as measurements in EvaluatedMetrics
    'charactersId': List[str],
    'metrics': EvaluatedMetrics
})

# all measurements from a set of simulations by metric
CharacterAllMeasurements = Dict[str, List[float]]

# CharacterAllMeasurements by characterId
CharactersAllMeasurements = Dict[str, CharacterAllMeasurements]

# Each metric accumulated for each character
MetricsByCharacter = Dict[str, Dict[str, float]]


class SimulationFitnessEvaluation(FitnessEvaluation, ABC):

    def __init__(
            self,
            metrics: List[str],
            desired_values: Dict[str, float],
            metrics_weights: Dict[str, float],
            queue_host: Optional[str] = None,
            queue_port: Optional[int] = None,
    ):

        if not set(metrics_weights.keys()) == set(desired_values.keys()) or not set(metrics) == set(metrics_weights.keys()):
            raise ValueError(
                "Not consistent metrics in metrics, metric weights and/or desired values")

        self.simulation_queue = SimulationQueue(
            **filter_not_none_values({
                'host': queue_host,
                'port': queue_port
            })
        )
        self.metrics = metrics
        self.metrics_weights = metrics_weights
        self.desired_values = desired_values

    def __call__(self, population: Population) -> EvaluatedPopulation:
        return self.evaluate_one_population(population)

    def evaluate_one_population(self, population: Population) -> EvaluatedPopulation:
        pass

    def simulate_population(
            self,
            population: Population,
            simulation_queue: SimulationQueue
    ) -> List[SimulationResult]:
        """
        Simulate characters in a way you choose and return simulation results
        """
        pass

    def evaluate_fitness_all_characters(
            self,
            characters_all_measurements: CharactersAllMeasurements
    ) -> Dict[str, float]:

        characters_metrics_score = self.evaluate_characters_metrics_score(
            characters_all_measurements)

        # combine metrics scores for each character by average and weight accordingly
        def metrics_score_to_fitness(metrics_score: Dict[str, float]) -> float:
            return mean([metrics_score[key]*self.metrics_weights[key] for key in metrics_score])/mean(self.metrics_weights.values())

        fitness_by_character: Dict[str, float] = {
            char_id: metrics_score_to_fitness(char_metrics_score)
            for char_id, char_metrics_score in characters_metrics_score.items()
        }

        return fitness_by_character

    def init_metric_values(self):
        return dict.fromkeys(self.desired_values, 0)

    def evaluate_characters_metrics_score(
            self,
            characters_all_measurements: CharactersAllMeasurements
    ) -> Dict[str, Dict[str, float]]:

        # give a score to each metric for each character
        characters_metrics_score: Dict[str, Dict[str, float]] = {
            char_id: {
                metric: self.evaluate_metric_score(
                    metric, measurements)
                for metric, measurements in char_measurements_by_metric.items()
            }
            for char_id, char_measurements_by_metric in characters_all_measurements.items()
        }

        return characters_metrics_score

    def evaluate_metric_score(self, metric, measurements: List[float]) -> float:
        if metric not in self.desired_values:
            raise ValueError("Evaluating a metric with no desired value")

        average_measurement = mean(measurements)

        return 1 - min(abs(self.desired_values[metric] - average_measurement) / self.desired_values[metric], 1)

    def simulation_results_to_simulation_measurements(
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

    def group_all_measures_by_character(
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
                        new_characters_measurements[char_id][metric].append(
                            measurement)

            return new_characters_measurements

        all_measurements_by_character = reduce(
            characters_measurements_reducer,
            simulations_measurements,
            {}  # start with an empty object
        )

        return all_measurements_by_character

    def serialize(self):
        config = {'metrics': self.metrics,
                  'desiredValues': self.desired_values, 'metricsWeights': self.metrics_weights}
        return config
