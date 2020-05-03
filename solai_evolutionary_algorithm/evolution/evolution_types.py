from typing import Callable, List, Tuple, TypedDict, Any


Individual = Any
Population = List[Individual]

EvaluatedIndividual = TypedDict("EvaluatedIndividual", {
    'individual': Individual,
    'fitness': List[float]
})

EvaluatedPopulation = List[EvaluatedIndividual]
SubPopulation = List[Individual]

FitnessFunc = Callable[[Individual], List[float]]

FitnessEvaluation = Callable[[Population], EvaluatedPopulation]

InitialPopulationProducer = Callable[[], Population]

PopulationEvolver = Callable[[EvaluatedPopulation], Population]

CrossoverStrategy = Callable[[Population], SubPopulation]

MutationStrategy = Callable[[Population], Population]

# determine if evolution should stop
EndCriteria = Callable[[], bool]

