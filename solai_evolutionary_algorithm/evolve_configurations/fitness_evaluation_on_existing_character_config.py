from solai_evolutionary_algorithm.crossovers.ability_swap_crossover import AbilitySwapCrossover
from solai_evolutionary_algorithm.evolution.novelty_and_fitness_evolver import NoveltyAndFitnessEvolver
from solai_evolutionary_algorithm.database.update_database_service import UpdateDatabaseService
from solai_evolutionary_algorithm.evaluation.fitness_archive import FitnessArchive
from solai_evolutionary_algorithm.evaluation.novel_archive import NovelArchive
from solai_evolutionary_algorithm.evaluation.simulation.from_existing_simulation_fitness_evaluation import \
    FromExistingSimulationFitnessEvaluation
from solai_evolutionary_algorithm.evolution.evolver_config import EvolverConfig
from solai_evolutionary_algorithm.evolution.novelty_and_fitness_evolver import NoveltyAndFitnessEvolver
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

character_properties_ranges = {"radius": [28.0, 50.0],
                               "moveVelocity": [200.0, 2000.0]}

melee_ability_ranges = {
    "name": "abilityName",
    "type": "MELEE",
    "radius": [16, 200],
    "distanceFromChar": [0, 200],
    "speed": [0, 0],
    "startupTime": [10, 500],
    "activeTime": [10, 60],
    "executionTime": [0, 60],
    "endlagTime": [10, 60],
    "rechargeTime": [0, 60],
    "damage": [100, 1000],
    "baseKnockback": [10, 1000],
    "knockbackRatio": [0.1, 1.0],
    "knockbackPoint": [-500, 500],
    "knockbackTowardPoint": [False, True]
}

projectile_ability_ranges = {
    "name": "abilityName",
    "type": "PROJECTILE",
    "radius": [5, 50],
    "distanceFromChar": [0, 200],
    "speed": [100, 800],
    "startupTime": [1, 60],
    "activeTime": [20, 1000],
    "executionTime": [0, 60],
    "endlagTime": [6, 60],
    "rechargeTime": [13, 80],
    "damage": [15, 500],
    "baseKnockback": [50, 1000],
    "knockbackRatio": [0.1, 1.0],
    "knockbackPoint": [-500, 500],
    "knockbackTowardPoint": [False, True]
}

from_existing_population_producer = FromExistingProducer(
    population_size=12,
    chars_filename=[
        "shrankConfig.json",
        "schmathiasConfig.json",
        "brailConfig.json",
        "magnetConfig.json"
    ]
)

novel_archive = NovelArchive(NovelArchive.Config(
    novel_archive_size=10,
    nearest_neighbour_number=4,
    character_properties_ranges=character_properties_ranges,
    melee_ability_ranges=melee_ability_ranges,
    projectile_ability_ranges=projectile_ability_ranges,
))

fitness_archive = FitnessArchive(FitnessArchive.Config(
    fitness_archive_size=50,
))

config = EvolverConfig(
    initial_population_producer=from_existing_population_producer,
    # fitness_evaluator=RandomFitnessEvaluation(),
    fitness_evaluator=FromExistingSimulationFitnessEvaluation(
        simulation_characters=from_existing_population_producer()[:4],
        metrics=["leadChange", "characterWon",
                 "stageCoverage", "nearDeathFrames", "gameLength", "hitInteractions"],
        metrics_weights={
            "leadChange": 0.4,
            "characterWon": 0.5,
            "stageCoverage": 0.5,
            "nearDeathFrames": 0.5,
            "gameLength": 1.0,
            "hitInteractions": 0.8
        },
        desired_values={
            "leadChange": 50,
            "characterWon": 0.6,
            "stageCoverage": 0.7,
            "nearDeathFrames": 700,
            "gameLength": 7200,
            "hitInteractions": 20
        },
        simulation_population_count=4,
        queue_host="localhost",
    ),
    # population_evolver=DefaultGenerationEvolver(DefaultGenerationEvolver.PassThroughConfig),
    population_evolver=NoveltyAndFitnessEvolver(NoveltyAndFitnessEvolver.Config(
        crossover_share=0.4,
        mutate_only_share=0.5,
        new_individuals_share=0,
        elitism_share=0.1,
        novel_archive=novel_archive,
        fitness_archive=fitness_archive,
        character_properties_ranges=character_properties_ranges,
        melee_ability_ranges=melee_ability_ranges,
        projectile_ability_ranges=projectile_ability_ranges,
        crossover=AbilitySwapCrossover(),
        mutations=[
            default_properties_mutation(
                probability_per_number_property=0.1,
                probability_per_bool_property=0.05,
                character_properties_ranges=character_properties_ranges,
                melee_ability_ranges=melee_ability_ranges,
                projectile_ability_ranges=projectile_ability_ranges
            )
        ],
        new_individuals_producer=[]
    )),
    end_criteria=FixedGenerationsEndCriteria(generations=150),
    evolver_listeners=[
        UpdateDatabaseService(),
        PlotGenerationsLocalService()
    ],
)
