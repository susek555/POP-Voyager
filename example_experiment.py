from experiment.runner import Experiment, ExperimentRunner
from graph.config import Graph, GraphScenario
from utils.config import Algorithm, AlgorithmParams, AlgorithmType

if __name__ == "__main__":
    from graph.generate import BasicGraphParams

    experiment = Experiment(
        name="test_random",
        graph=Graph(
            scenario=GraphScenario.BASIC,
            params=BasicGraphParams(
                number_of_nodes=20, max_base_distance=50.0, reward_range=(5, 20), cost_factor=0.1
            ),
        ),
        algorithm=Algorithm(
            type=AlgorithmType.RANDOM,
            params=AlgorithmParams(),
        ),
        max_nodes=10,
        times_to_run=5,
    )

    runner = ExperimentRunner(experiment)
    runner.perform()
