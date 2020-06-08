from typing import Callable, List, Tuple, TypedDict, Any, Optional


Individual = Any
Population = List[Individual]

EvaluatedIndividual = TypedDict("EvaluatedIndividual", {
    'individual': Individual,
    'fitness': float,
    'feasibility_score': float,
    'novelty': float
})

# NoveltyAndFitnessEvaluatedIndividual = TypedDict("EvaluatedIndividual", {
#     'individual': Individual,
#     'fitness': List[float],
#     'novelty': float
# })

NoveltyAndFitnessEvaluatedPopulation = List[EvaluatedIndividual]
EvaluatedPopulation = List[EvaluatedIndividual]
SubPopulation = List[Individual]

FitnessEvaluation = Callable[[Population], EvaluatedPopulation]

InitialPopulationProducer = Callable[[], Population]

PopulationEvolver = Callable[[EvaluatedPopulation], Population]

CrossoverStrategy = Callable[[Population], SubPopulation]

MutationStrategy = Callable[[Population], Population]

# determine if evolution should stop
EndCriteria = Callable[[], bool]
