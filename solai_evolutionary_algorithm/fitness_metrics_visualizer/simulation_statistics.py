from dataclasses import dataclass
from statistics import mean
from typing import Dict, List, cast

from solai_evolutionary_algorithm.evaluation.simulation.constrained_novelty_evaluation import \
    ConstrainedNoveltyEvaluation
from solai_evolutionary_algorithm.evaluation.simulation.simulation_all_vs_all_fitness_evaluation import \
    SimulationAllVsAllFitnessEvaluation
from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation, Population, EvaluatedIndividual



@dataclass(frozen=True)
class CharacterSimulationStatistics:
    evaluations: EvaluatedIndividual
    measurements: Dict[str, float]


def repeat_simulate_statistics(
        chars: List[CharacterConfig],
        evaluator: ConstrainedNoveltyEvaluation,
        repeat: int,
) -> List[List[CharacterSimulationStatistics]]:

    population: Population = chars

    def average_evaluations(measurements_by_metric):
        return {
            metric: mean(measurements)
            for metric, measurements in measurements_by_metric.items()
        }

    def evaluate_and_retrieve_statistics(evaluator, population):
        evaluated_population = evaluator(population)
        measures_by_character_id = evaluator.get_prev_measures_by_character_id()
        return [
            CharacterSimulationStatistics(
                evaluations=evaluated_character,
                measurements=average_evaluations(
                    measures_by_character_id[evaluated_character['individual']['characterId']])
            )
            for evaluated_character in evaluated_population
        ]

    all_statistics = [
        evaluate_and_retrieve_statistics(evaluator, population)
        for _ in range(repeat)
    ]

    return all_statistics

    # fitnesses_by_char_id: Dict[str, List[float]] = {
    #     char['characterId']: []
    #     for char in chars
    # }
    #
    # metrics_score_by_char_id: Dict[str, Dict[str, List[float]]] = {
    #     char['characterId']: {
    #         metric: []
    #         for metric in metrics
    #     }
    #     for char in chars
    # }
    #
    # avr_measurements_by_char_id: Dict[str, Dict[str, List[float]]] = {
    #     char['characterId']: {
    #         metric: []
    #         for metric in metrics
    #     }
    #     for char in chars
    # }
    #
    # for i in range(repeat):
    #     population = chars
    #     print(f"Running population evaluation {i}")
    #     evaluated_population: EvaluatedPopulation = simulation_evaluator(
    #         population)
    #     simulation_results = simulation_evaluator.get_prev_simulation_results()
    #     measurements_by_char_id = simulation_evaluator.get_prev_measures_by_character_id()
    #
    #     for char_id, measurements_by_metric in measurements_by_char_id.items():
    #         avr_measurements_by_metric = {
    #             metric: mean(measurements)
    #             for metric, measurements in measurements_by_metric.items()
    #         }
    #
    #         avr_measurements_by_char_id[char_id] = {
    #             metric: prev_avr_measurements + [avr_measurement]
    #             for (metric, avr_measurement), prev_avr_measurements in zip(
    #                 avr_measurements_by_metric.items(),
    #                 avr_measurements_by_char_id[char_id].values()
    #             )
    #         }
    #
    #         metric_scores = {
    #             metric: simulation_evaluator.evaluate_metric_score(
    #                 metric, measurements)
    #             for metric, measurements in measurements_by_metric.items()
    #         }
    #
    #         metrics_score_by_char_id[char_id] = {
    #             metric: prev_metric_scores + [metric_score]
    #             for (metric, metric_score), prev_metric_scores in zip(
    #                 metric_scores.items(),
    #                 metrics_score_by_char_id[char_id].values()
    #             )
    #         }
    #
    #     for evaluated_char in evaluated_population:
    #         char = evaluated_char['individual']
    #         fitness = sum(evaluated_char['fitness'])
    #         fitnesses_by_char_id[char['characterId']].append(fitness)
    #
    # return SimulationStatistics(
    #     characters_config_by_char_id= {
    #         char['characterId']: char
    #         for char in chars
    #     },
    #     fitnesses_by_char_id=fitnesses_by_char_id,
    #     metrics_score_by_char_id=metrics_score_by_char_id,
    #     avr_measurements_by_char_id=avr_measurements_by_char_id
    # )
