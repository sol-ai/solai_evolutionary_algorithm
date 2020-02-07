from representation.representation import Representation
from evolution.evolution import Evolution

def main():
    init_poplation_size = 20
    representation = Representation()
    init_population = representation.generate_initial_population(init_poplation_size)
    evolution = Evolution(init_population)
    evolution.evolve()
    fittest_individuals = evolution.get_fittest_individuals()
    return fittest_individuals

if __name__ == "__main__":
    main()