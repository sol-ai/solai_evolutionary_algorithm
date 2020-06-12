from enum import Enum
from statistics import mean
from typing import List, Optional, Dict, Tuple, Callable, Union

from solai_evolutionary_algorithm.evaluation.simulation.novelty_handling import \
    calculate_distance_and_update_novel_archive, IndividualsWithDistance, NovelArchive
from solai_evolutionary_algorithm.evaluation.simulation.simulation_fitness_evaluation import \
    SimulationFitnessEvaluation, \
    CharacterAllMeasurements, CharactersAllMeasurements
from solai_evolutionary_algorithm.evaluation.simulation.simulation_queue import SimulationQueue, SimulationData, \
    CharacterConfig, SimulationResult
from solai_evolutionary_algorithm.evolution.evolution_types import Individual
from solai_evolutionary_algorithm.evolution.evolution_types import Population, EvaluatedPopulation, \
    EvaluatedIndividual
from solai_evolutionary_algorithm.utils.kwargs_utils import filter_not_none_values


class InfeasibleObjective(Enum):
    NOVELTY = "NOVELTY"
    FEASIBILITY = "FEASIBILITY"


class ConstrainedNoveltyEvaluation(SimulationFitnessEvaluation):

    """
    feasible_metric_ranges: The ranges of a simulation result that determines an individual feasible or infeasible.
    minimum_required_feasible_metric_percentage: The percentage of metrics that must fall into the feasible metric ranges.
    """

    def __init__(
            self,
            metrics: List[str],
            simulation_characters: List,
            feasible_metric_ranges: Dict[str, Tuple],
            distance_func: Callable[[Individual, Individual], float],
            consider_closest_count: int,
            insert_most_novel_count: int,
            infeasible_objective: InfeasibleObjective,
            queue_host: Optional[str] = None,
            queue_port: Optional[str] = None,
            minimum_required_feasible_metric_percentage: Optional[float] = 1.0,
            simulation_population_count: Optional[int] = 1,
        ):

        self.metrics = metrics
        self.simulation_characters = simulation_characters
        self.feasible_metric_ranges = feasible_metric_ranges
        self.distance_func = distance_func
        self.consider_closest_count = consider_closest_count
        self.insert_most_novel_count = insert_most_novel_count
        self.infeasible_objective = infeasible_objective

        self.feasible_novel_archive: List[Individual] = []
        if infeasible_objective == InfeasibleObjective.NOVELTY:
            self.infeasible_novel_archive: List[Individual] = []

        self.simulation_queue = SimulationQueue(
            **filter_not_none_values({
                'host': queue_host,
                'port': queue_port
            })
        )

        self.minimum_required_feasible_metric_percentage = minimum_required_feasible_metric_percentage
        self.simulation_population_count = simulation_population_count

        self.__prev_measures_by_character_id: CharactersAllMeasurements = {}

    def __call__(self, population: Population) -> EvaluatedPopulation:
        return self.evaluate_one_population(population)

    def get_prev_measures_by_character_id(self) -> CharactersAllMeasurements:
        return self.__prev_measures_by_character_id

    def evaluate_one_population(self, population: Population) -> EvaluatedPopulation:
        simulations_results = self.simulate_population(
            population, self.simulation_queue)

        simulations_measurements = self.simulation_results_to_simulation_measurements(
            simulations_results)

        all_measurements_by_character: CharactersAllMeasurements = self.group_all_measures_by_character(
            simulations_measurements)

        self.__prev_measures_by_character_id = all_measurements_by_character

        feasibility_by_character_id: Dict[str, float] = self.evaluate_feasibility_of_population(
            all_measurements_by_character)

        feasible_population = [
            character
            for character in population
            if feasibility_by_character_id[character['characterId']] == 1
        ]
        infeasible_population = [
            character
            for character in population
            if feasibility_by_character_id[character['characterId']] != 1
        ]

        novelty_by_feasible_character_id, self.feasible_novel_archive = self.evaluate_novelty(
            feasible_population,
            self.feasible_novel_archive
        )

        feasible_evaluated_population = [
            EvaluatedIndividual(
                individual=character,
                fitness=[-1],
                feasibility_score=feasibility_by_character_id[character['characterId']],
                novelty=novelty_by_feasible_character_id[character['characterId']]
            )
            for character in feasible_population
        ]

        if self.infeasible_objective == InfeasibleObjective.NOVELTY:
            novelty_by_infeasible_character_id, self.infeasible_novel_archive = self.evaluate_novelty(
                infeasible_population,
                self.infeasible_novel_archive
            )

            infeasible_evaluated_population = [
                EvaluatedIndividual(
                    individual=character,
                    fitness=[-1],
                    feasibility_score=feasibility_by_character_id[character['characterId']],
                    novelty=novelty_by_infeasible_character_id[character['characterId']]
                )
                for character in infeasible_population
            ]
        else:
            infeasible_evaluated_population = [
                EvaluatedIndividual(
                    individual=character,
                    fitness=[-1],
                    feasibility_score=feasibility_by_character_id[character['characterId']],
                    novelty=-1
                )
                for character in infeasible_population
            ]

        evaluated_population = feasible_evaluated_population + infeasible_evaluated_population
        return evaluated_population

    def evaluate_novelty(
            self,
            population: Population,
            novel_archive: NovelArchive
    ) -> Tuple[Dict[str, float], NovelArchive]:
        individuals_with_distance, novel_archive = calculate_distance_and_update_novel_archive(
            population,
            novel_archive,
            distance_func=self.distance_func,
            distance_consider_count=self.consider_closest_count,
            insert_most_novel_count=self.insert_most_novel_count
        )

        distance_by_character_id: Dict[str, float] = {
            character['characterId']: distance
            for character, distance in individuals_with_distance
        }

        return distance_by_character_id, novel_archive


    def simulate_population(self, population: Population, simulation_queue: SimulationQueue) -> List[SimulationResult]:

        character_pairs: List[Tuple[CharacterConfig, CharacterConfig]] = [
            (individual, opponent)
            for opponent in self.simulation_characters
            for individual in population
        ]

        all_simulation_pairs = self.simulation_population_count*character_pairs

        current_simulations_data = [
            SimulationData(
                simulationId=simulation_queue.create_simulation_id(),
                charactersConfigs=char_pair,
                metrics=self.metrics
            )
            for char_pair in all_simulation_pairs
        ]

        print(
            f"Pushing {len(current_simulations_data)} simulations, waiting for simulation results...\n\n")
        simulations_result = simulation_queue.push_simulations_data_wait_results(
            current_simulations_data)

        return simulations_result

    def evaluate_feasibility_of_population(
            self,
            measurements_by_character: CharactersAllMeasurements
    ) -> Dict[str, float]:
        evaluated_population = {
            characterId: self.feasibility_score(measurements_by_metric)
            for characterId, measurements_by_metric in measurements_by_character.items()
        }
        return evaluated_population

    def feasibility_score(self, character_simulation_result: CharacterAllMeasurements) -> float:
        mean_simulation_results = {
            metric: mean(measurements)
            for (metric, measurements) in character_simulation_result.items()
        }
        feasible_number = sum([
            self.is_feasible_metric_result(metric, metric_result)
            for metric, metric_result in mean_simulation_results.items()
        ])

        metrics_count = len(character_simulation_result)
        return feasible_number / metrics_count

    def is_feasible_metric_result(self, metric: str, metric_result: float) -> bool:
        feasible_metric_range = self.feasible_metric_ranges[metric]
        return feasible_metric_range[0] <= metric_result <= feasible_metric_range[1]

    def serialize(self):
        config = {'metrics': self.metrics,
                  'feasibilityRanges': self.feasible_metric_ranges}
        return config
