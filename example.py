import logging

from graph.draw import draw_graph

# from graph.scenarios.siren_song import generate_siren_song_graph
# from graph.scenarios.bottleneck import generate_bottleneck_graph
# from graph.scenarios.nebula import generate_nebula_graph
from graph.generate import BasicGraphParams, generate_graph

# from graph.scenarios.archipelago import generate_archipelago_graph
from graph.scenarios.line_circle import LineCircleGraphParams, generate_line_circle_graph
from utils.logger import setup_logger

setup_logger(logging.INFO)
# Disable <= CRITICAL logs from imported functions
# logging.disable(logging.CRITICAL)

G = generate_graph(BasicGraphParams())
G = generate_line_circle_graph(
    LineCircleGraphParams(
        n_nodes_line=10,
        n_nodes_circle=20,
        line_dist=1.0,
        circle_radius=500.0,
        reward_range=(10, 100),
        cost_factor=0.6,
        circle_multiplier=100.0,
    )
)
# G = generate_archipelago_graph(
#     n_clusters=4,
#     nodes_per_cluster=8,
#     cluster_spread=10.0,
#     map_size=100.0,
#     reward_range=(20, 1000),
#     cost_factor=0.2
# )
# G = generate_siren_song_graph(
#     n_local_nodes=30,
#     local_dist_range=(5.0, 20.0),
#     local_reward_range=(5, 15),
#     siren_distance=150.0,
#     siren_reward=800,
#     cost_factor=0.2
# )
# G = generate_bottleneck_graph(
#     nodes_per_side=20,
#     bridge_nodes=1,
#     side_distance=50.0,
#     bubble_radius=15.0,
#     reward_range=(20, 80),
#     far_reward_multiplier=3.0,
#     cost_factor=0.2
# )
# G = generate_nebula_graph(
#     n_nodes=50,
#     cloud_radius=70.0,
#     nebula_center=(30.0, 0.0, 0.0),
#     nebula_radius=20.0,
#     nebula_multiplier=4.0,
#     reward_range=(15, 60),
#     cost_factor=0.2
# )
# G = generate_gradient_graph(
#     n_nodes=60,
#     max_dist=120.0,
#     base_reward=15,
#     reward_scaling=8.0,
#     cost_factor=0.2
# )

paths = {}
evals = {}

# path = full_random(G, 10, AlgorithmParams())
# print(f"Random: {objective_function(G, path)}")
# paths["Random"] = path
# evals["Random"] = objective_function(G, path)

# path = greedy(G, 10)
# print(f"Greedy: {objective_function(G, path)}")
# greedy_eval = objective_function(G, path)
# paths["Greedy"] = path
# evals["Greedy"] = objective_function(G, path)

# path = SA(
#     G,
#     objective_function,
#     10,
#     SAparams(
#         n_iter=5000,
#         start_temp=100.0,
#         decrease_factor=0.99,
#         n_threads=4,
#         n_candidates_per_thread=4,
#     ),
# )
# print(f"SA: {objective_function(G, path)}")
# paths["SA"] = path
# evals["SA"] = objective_function(G, path)

# path = genetic(
#     G,
#     objective_function,
#     10,
#     GeneticParams(
#         pop_size=50,
#         generations=200,
#         mutation_rate=0.15,
#         crossover=ordered_crossover,
#         selection=select_tournament,
#         selection_kwargs={"tournament_size": 3},
#     ),
# )
# print(f"Genetic: {objective_function(G, path)}")
# paths["Genetic"] = path
# evals["Genetic"] = objective_function(G, path)

# path = aco(
#     G,
#     objective_function,
#     10,
#     AcoParams(
#         ant_count=100,
#         iteration_count=400,
#         alpha=1,
#         beta=2,
#         pheromone_degradation_rate=0.1,
#         Q=300,
#         candidate_list_size=60,
#     ),
#     stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
# )
# print(f"ACO: {objective_function(G, path)}")
# paths["ACO"] = path
# evals["ACO"] = objective_function(G, path)

# path = aco(
#     G,
#     objective_function,
#     10,
#     AcoParams(
#         ant_count=100,
#         iteration_count=400,
#         alpha=1.5,
#         beta=2.5,
#         pheromone_degradation_rate=0.15,
#         Q=300,
#         candidate_list_size=60,
#         deposit_mode="diffusion",
#         diffusion_range=1,
#     ),
#     stagnation_strategy=utils.ant_colony.stagnation_strategies.EarlyStoppingStrategy(200),
# )
# print(f"ACO (diffused): {objective_function(G, path)}")
# paths["ACO (diffused)"] = path
# evals["ACO (diffused)"] = objective_function(G, path)

# path = A_star(G, 10, greedy_eval)
# print(f"A_star: {objective_function(G, path)}")
# path = A_star(G, 10, greedy_eval, childrenFactory=ChildrenFactory.N_BEST, n_children=10)
# print(f"Quazi A_star: {objective_function(G, path)}")
# paths["A*_greedy"] = path
# evals["A*_greedy"] = objective_function(G, path)

draw_graph(G, "Example 3D Graph", paths, evals)
