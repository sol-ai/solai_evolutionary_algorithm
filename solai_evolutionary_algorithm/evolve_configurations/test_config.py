from solai_evolutionary_algorithm.crossovers.ability_swap_crossover import AbilitySwapCrossover
from solai_evolutionary_algorithm.database.update_database_service import UpdateDatabaseService
from solai_evolutionary_algorithm.evaluation.simulation.simulation_fitness_evaluation import SimulationFitnessEvaluation
from solai_evolutionary_algorithm.evolution.evolver_config import EvolverConfig
from solai_evolutionary_algorithm.evolution.generation_evolver import DefaultGenerationEvolver
from solai_evolutionary_algorithm.evolution_end_criteria.fixed_generation_end_criteria import \
    FixedGenerationsEndCriteria
from solai_evolutionary_algorithm.initial_population_producers.from_existing_producers import FromExistingProducer
from solai_evolutionary_algorithm.initial_population_producers.random_bounded_producer import RandomBoundedProducer
from solai_evolutionary_algorithm.mutations.default_properties_mutation import default_properties_mutation
from solai_evolutionary_algorithm.plot_services.plot_generations_service import PlotGenerationsLocalService

random_population_producer = RandomBoundedProducer(RandomBoundedProducer.Config(
    population_size=20,
    character_properties_ranges={},
    melee_ability_ranges={},
    projectile_ability_ranges={}
))

from_existing_population_producer = FromExistingProducer(
    population_size=12,
    chars_filename=[
        "shrankConfig.json",
        "schmathiasConfig.json",
        "brailConfig.json",
        "magnetConfig.json"
    ]
)

test_config = EvolverConfig(
    initial_population_producer=from_existing_population_producer,
    # fitness_evaluator=RandomFitnessEvaluation(),
    fitness_evaluator=SimulationFitnessEvaluation(
        metrics=["leadChange", "characterWon",
                 "stageCoverage", "nearDeathFrames", "gameLength"],
        queue_host="localhost",
        desired_values={
            "leadChange": 50,
            "characterWon": 0.8,
            "stageCoverage": 0.7,
            "nearDeathFrames": 700,
            "gameLength": 7200
        }
    ),
    # population_evolver=DefaultGenerationEvolver(DefaultGenerationEvolver.PassThroughConfig),
    population_evolver=DefaultGenerationEvolver(DefaultGenerationEvolver.Config(
        crossover_share=0.2,
        mutate_only_share=0.7,
        new_individuals_share=0,
        elitism_share=0.1,
        crossover=AbilitySwapCrossover(),
        mutations=[
            default_properties_mutation(
                probability_per_number_property=0.1,
                probability_per_bool_property=0.05,
            )
        ]
    )),
    end_criteria=FixedGenerationsEndCriteria(generations=10),
    evolver_listeners=[
        # UpdateDatabaseService(),
        PlotGenerationsLocalService()
    ],
)
