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



random_population_producer = RandomBoundedProducer(RandomBoundedProducer.Config(
    population_size=20,
    character_properties_ranges=character_properties_ranges,
    melee_ability_ranges=melee_ability_ranges,
    projectile_ability_ranges=projectile_ability_ranges
))

from_existing_population_producer = FromExistingProducer(
    population_size=8,
    chars_filename=[
        "shrankConfig.json",
        "schmathiasConfig.json",
        "brailConfig.json",
        "magnetConfig.json"
    ]
)

novel_archive = NovelArchive(NovelArchive.Config(
    novel_archive_size=20,
    nearest_neighbour_number=4,
    character_properties_ranges=character_properties_ranges,
    melee_ability_ranges=melee_ability_ranges,
    projectile_ability_ranges=projectile_ability_ranges,
))

fitness_archive = FitnessArchive(FitnessArchive.Config(
    fitness_archive_size=50,
))

fitness_archive_config = EvolverConfig(
    initial_population_producer=from_existing_population_producer,
    # fitness_evaluator=RandomFitnessEvaluation(),
    fitness_evaluator=FromExistingSimulationFitnessEvaluation(
        simulation_characters=from_existing_population_producer()[:4],
        metrics=["leadChange", "characterWon",
                 "stageCoverage", "nearDeathFrames", "gameLength", "hitInteractions"],
        metrics_weights={
            "leadChange": 0.0,
            "characterWon": 1.0,
            "stageCoverage": 0.0,
            "nearDeathFrames": 0.0,
            "gameLength": 1.0,
            "hitInteractions": 0.0,
        },
        desired_values={
            "leadChange": 50,
            "characterWon": 0.5,
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
        crossover_share=0.8,
        mutate_only_share=0.1,
        new_individuals_share=0.0,
        elitism_share=0.1,
        novel_archive=novel_archive,
        fitness_archive=fitness_archive,
        character_properties_ranges=character_properties_ranges,
        melee_ability_ranges=melee_ability_ranges,
        projectile_ability_ranges=projectile_ability_ranges,
        crossover=AbilitySwapCrossover(),
        mutations=[
            default_properties_mutation(
                character_properties_ranges=character_properties_ranges,
                melee_ability_ranges=melee_ability_ranges,
                projectile_ability_ranges=projectile_ability_ranges,
                probability_per_number_property=0.5,
                probability_per_bool_property=0.05,
            )
        ],
        new_individuals_producer=random_population_producer
    )),
    end_criteria=FixedGenerationsEndCriteria(generations=10),
    evolver_listeners=[
        UpdateDatabaseService(),
        # PlotGenerationsLocalService()
    ],
)
