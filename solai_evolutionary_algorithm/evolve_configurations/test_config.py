from solai_evolutionary_algorithm.crossovers.ability_swap_crossover import AbilitySwapCrossover
from solai_evolutionary_algorithm.evaluation.random_fitness_evaluation import RandomFitnessEvaluation
from solai_evolutionary_algorithm.evaluation.simulation.simulation_fitness_evaluation import SimulationFitnessEvaluation
from solai_evolutionary_algorithm.evolution.evolver import EvolverConfig, FixedGenerationsEndCriteria
from solai_evolutionary_algorithm.evolution.generation_evolver import DefaultGenerationEvolver
from solai_evolutionary_algorithm.initial_population_producers.random_bounded_producer import RandomBoundedProducer
from solai_evolutionary_algorithm.database.database import Database


test_config = EvolverConfig(
    initial_population_producer=RandomBoundedProducer(RandomBoundedProducer.Config(
        population_size=3,
        character_properties_ranges={},
        melee_ability_ranges={},
        projectile_ability_ranges={}
    )),
    # fitness_evaluator=RandomFitnessEvaluation(),
    fitness_evaluator=SimulationFitnessEvaluation(
        metrics=["leadChange", "characterWon",
                 "stageCoverage", "nearDeathFrames", "gameLength"],
        queue_host="localhost"
    ),
    # population_evolver=DefaultGenerationEvolver(DefaultGenerationEvolver.PassThroughConfig),
    population_evolver=DefaultGenerationEvolver(DefaultGenerationEvolver.Config(
        crossover_share=0.6,
        elitism_share=0.4,
        new_individuals_share=0,
        crossover=AbilitySwapCrossover(),
        mutations=[],
        new_individuals_producer=None
    )),
    end_criteria=FixedGenerationsEndCriteria(generations=3),
    database=Database()
)
