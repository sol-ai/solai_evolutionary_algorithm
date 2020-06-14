import json
from itertools import combinations
from typing import List, Dict, Optional, cast

import matplotlib.pyplot as plt

from solai_evolutionary_algorithm.evaluation.simulation.constrained_novelty_evaluation import \
    ConstrainedNoveltyEvaluation
from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import CharacterConfig
from solai_evolutionary_algorithm.evolve_configurations import constrained_novelty_config
from solai_evolutionary_algorithm.fitness_metrics_visualizer.simulation_statistics import repeat_simulate_statistics
from solai_evolutionary_algorithm.initial_population_producers.from_existing_producers import load_char_from_file
from solai_evolutionary_algorithm.plot_services.plot_generations_service import PlotGenerationsLocalService
from solai_evolutionary_algorithm.utils.character_id import create_character_id


def plot_metrics_values_by_char_grouped(title: str, chars_name: List[str], chars_metrics_value_by_metric: List[Dict[str, List[float]]]):
    fig, axis_grid = plt.subplots(2, 2, constrained_layout=True)
    fig.suptitle(title)
    axis = axis_grid.reshape(-1)
    for plot_axes, char_name, metric_values_by_metric in zip(
            axis,
            chars_name,
            chars_metrics_value_by_metric
    ):
        plot_axes.set_title(char_name)
        metrics = list(metric_values_by_metric.keys())
        measurements = list(metric_values_by_metric.values())
        plot_axes.set_xticklabels(metrics, rotation=20, ha='right')
        plot_axes.boxplot(measurements)


def plot_metrics_values_by_char_individually(
        title: str,
        chars_name: List[str],
        chars_metrics_value_by_metric: List[Dict[str, List[float]]],
        baseline_metrics_value: Optional[Dict[str, float]] = None
):
    char_count = len(chars_name)
    metrics = list(chars_metrics_value_by_metric[0].keys())
    metrics_count = len(metrics)
    fig, axis_grid = plt.subplots(
        metrics_count, char_count, constrained_layout=True)

    for ax, char_name in zip(axis_grid[0], chars_name):
        ax.set_title(char_name, rotation=0, size='large')

    for ax, metric in zip(axis_grid[:, 0], metrics):
        ax.set_ylabel(metric, rotation=0, size='large', ha='right')

    for plot_metrics_axis, char_name, metric_values_by_metric in zip(
            axis_grid.T,
            chars_name,
            chars_metrics_value_by_metric
    ):
        for plot_metric_axes, (metric, metric_values) in zip(plot_metrics_axis, metric_values_by_metric.items()):
            if baseline_metrics_value is not None:
                plot_metric_axes.plot(
                    [1], [baseline_metrics_value[metric]], 'r_')
            plot_metric_axes.boxplot(
                [metric_values], showmeans=True, meanline=True)
            plot_metric_axes.set_xticks([])

    fig.suptitle(title)


def save_statistics(
        filename: str,
        chars_name: List[str],
        chars_metrics_value_by_metric: List[Dict[str, List[float]]]
):
    values_by_char_name = {
        char_name: measurements_by_metric
        for char_name, measurements_by_metric in zip(chars_name, chars_metrics_value_by_metric)
    }
    file = open(f"files/{filename}", 'w')
    json.dump(values_by_char_name, file)


def visualize_metrics(chars: List[CharacterConfig]):
    repeat = 100

    evaluator = cast(ConstrainedNoveltyEvaluation,
                     constrained_novelty_config.constrained_novelty_config.fitness_evaluator)

    chars_by_id = {
        char['characterId']: char
        for char in chars
    }

    all_statistics = repeat_simulate_statistics(
        list(chars_by_id.values()),
        evaluator=evaluator,
        repeat=repeat
    )

    metrics = all_statistics[0][0].measurements.keys()

    metric_measurements_by_character_id = {
        char['characterId']: {
            **{
                metric: []
                for metric in metrics
            },
            'feasibility_score': [],
        }
        for char in chars
    }
    for pop_statistics in all_statistics:
        for ind_statistics in pop_statistics:
            character_id = ind_statistics.evaluations['individual']['characterId']
            feasibility_score = ind_statistics.evaluations['feasibility_score']
            character_metric_measurements = metric_measurements_by_character_id[character_id]
            for metric, measurement in ind_statistics.measurements.items():
                character_metric_measurements[metric].append(measurement)
            character_metric_measurements['feasibility_score'].append(
                feasibility_score)

    char_names = [
        chars_by_id[charId]['name']
        for charId in metric_measurements_by_character_id.keys()
    ]

    pair_simulation_count = evaluator.simulation_population_count
    plot_title = f"Average measurements over {repeat} runs, with populations simulated {pair_simulation_count} times"

    save_statistics(
        f"{plot_title.replace(' ', '_')}.json",
        chars_name=char_names,
        chars_metrics_value_by_metric=list(
            metric_measurements_by_character_id.values())
    )

    plot_metrics_values_by_char_individually(
        plot_title,
        chars_name=char_names,
        chars_metrics_value_by_metric=list(
            metric_measurements_by_character_id.values())
    )

    plt.show()


if __name__ == '__main__':
    chars_filename = [
        "existing_characters/shrankConfig.json",
        "existing_characters/schmathiasConfig.json",
        "existing_characters/brailConfig.json",
        "existing_characters/magnetConfig.json"
    ]
    char_configs = [
        {**load_char_from_file(char_filename),
         'characterId': create_character_id()}
        for char_filename in chars_filename
    ]

    visualize_metrics(char_configs)
