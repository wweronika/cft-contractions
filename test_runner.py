from entropy_graph import EntropyGraph
from squares_graph import SquaresGraphL1R1, SquaresGraphL1R0, SquaresGraphL0R1, SquaresGraphL0R0
from graph_manipulations import test_all_orderings, check_all_outputs_same
from test_matchings import matchings_of_entropy_graph, check_all_perfect_matchings


n = 2
graph = EntropyGraph(n)

results = test_all_orderings(
    graph,
    "v_top_left_0",
    "v_top_middle_0",
    ["v_bottom_left_0", "v_top_right_1"],
    ["v_middle_middle_0", "v_top_right_0"],
)

print(check_all_outputs_same(results))

def print_results(results):
    for r in results:
        print(
            f"inner_swap={r['swap_inner']}, "
            f"n1_swap={r['swap_neigh1']}, "
            f"n2_swap={r['swap_neigh2']}"
        )
        print(f"input : {r['input']}")
        print(f"output: {r['output']}")
        print("-" * 50)

print_results(results)

ms = matchings_of_entropy_graph(n)
print(f"Wick contractions for n=1{n}: ")
check_all_perfect_matchings(graph, ms)