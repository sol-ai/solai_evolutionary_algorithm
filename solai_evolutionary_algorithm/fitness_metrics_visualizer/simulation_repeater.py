from dataclasses import dataclass
from statistics import mean
from typing import Dict, List

from solai_evolutionary_algorithm.evaluation.simulation.simulation_all_vs_all_fitness_evaluation import SimulationAllVsAllFitnessEvaluation
from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolution.evolution_types import EvaluatedPopulation


@dataclass(frozen=True)
class RepeatSimulationData:
    fitnesses_by_char_id: Dict[str, List[float]]
    metrics_score_by_char_id: Dict[str, Dict[str, List[float]]]
    # average measurement for each evaluated population
    avr_measurements_by_char_id: Dict[str, Dict[str, List[float]]]


def repeat_simulate(
        chars: List[CharacterConfig],
        metrics_desired_values: Dict[str, float],
        metrics_weights: Dict[str, float],
        repeat: int,
) -> RepeatSimulationData:

    metrics = list(metrics_desired_values.keys())

    simulation_evaluator = SimulationAllVsAllFitnessEvaluation(
        metrics_weights=metrics_weights,
        simulation_population_count=20,
        metrics=metrics,
        queue_host="localhost",
        desired_values=metrics_desired_values
    )

    fitnesses_by_char_id: Dict[str, List[float]] = {
        char['characterId']: []
        for char in chars
    }

    metrics_score_by_char_id: Dict[str, Dict[str, List[float]]] = {
        char['characterId']: {
            metric: []
            for metric in metrics
        }
        for char in chars
    }

    avr_measurements_by_char_id: Dict[str, Dict[str, List[float]]] = {
        char['characterId']: {
            metric: []
            for metric in metrics
        }
        for char in chars
    }

    for i in range(repeat):
        population = chars
        print(f"Running population evaluation {i}")
        evaluated_population: EvaluatedPopulation = simulation_evaluator(
            population)
        simulation_results = simulation_evaluator.get_prev_simulation_results()
        measurements_by_char_id = simulation_evaluator.get_prev_measures_by_character_id()

        for char_id, measurements_by_metric in measurements_by_char_id.items():
            avr_measurements_by_metric = {
                metric: mean(measurements)
                for metric, measurements in measurements_by_metric.items()
            }

            avr_measurements_by_char_id[char_id] = {
                metric: prev_avr_measurements + [avr_measurement]
                for (metric, avr_measurement), prev_avr_measurements in zip(
                    avr_measurements_by_metric.items(),
                    avr_measurements_by_char_id[char_id].values()
                )
            }

            metric_scores = {
                metric: simulation_evaluator.evaluate_metric_score(
                    metric, measurements)
                for metric, measurements in measurements_by_metric.items()
            }

            metrics_score_by_char_id[char_id] = {
                metric: prev_metric_scores + [metric_score]
                for (metric, metric_score), prev_metric_scores in zip(
                    metric_scores.items(),
                    metrics_score_by_char_id[char_id].values()
                )
            }

        for evaluated_char in evaluated_population:
            char = evaluated_char['individual']
            fitness = sum(evaluated_char['fitness'])
            fitnesses_by_char_id[char['characterId']].append(fitness)

    return RepeatSimulationData(
        fitnesses_by_char_id=fitnesses_by_char_id,
        metrics_score_by_char_id=metrics_score_by_char_id,
        avr_measurements_by_char_id=avr_measurements_by_char_id
    )
