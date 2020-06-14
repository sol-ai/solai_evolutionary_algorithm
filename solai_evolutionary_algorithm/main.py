from solai_evolutionary_algorithm.evaluation.simulation.constrained_novelty_evaluation import InfeasibleObjective
from solai_evolutionary_algorithm.evolution.evolver import Evolver, EvolverConfig
from solai_evolutionary_algorithm.evolve_configurations import constrained_novelty_config


def main():
    population_size = 40
    generations = 30
    feasible_boost = True
    simulation_population_count = 10

    params = [
        {
            'initial_population': "random",
            'infeasible_objective': InfeasibleObjective.FEASIBILITY
        },
        {
            'initial_population': "from_existing",
            'infeasible_objective': InfeasibleObjective.FEASIBILITY
        },
        {
            'initial_population': "random",
            'infeasible_objective': InfeasibleObjective.NOVELTY
        },
        {
            'initial_population': "from_existing",
            'infeasible_objective': InfeasibleObjective.NOVELTY
        },
    ]

    i = 2
    while True:
        use_params = params[i % len(params)]

        evolver = Evolver()
        config = constrained_novelty_config.config(
            population_size=population_size,
            generations=generations,
            initial_population=use_params['initial_population'],
            infeasible_objective=use_params['infeasible_objective'],
            feasible_boost=feasible_boost,
            simulation_population_count=simulation_population_count
        )
        evolver.evolve(config)

        i += 1
