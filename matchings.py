
from draw_graphs import save_entropy_graph_with_highlighted_edges, save_squares_graph_with_highlighted_edges
from entropy_graph import *
from squares_graph import *

def matchings_of_L1R1_graph(n):
    if n == 0:
        return matchings_L1R1_zero_case()
    if n == 1:
        return matchings_L1R1_base_case()
    else:
        edges_to_append_1 = [f"e_top_left_half_{2 * n - 2}", 
                          f"e_bottom_{2 * n - 2}",
                          f"e_top_between_squares_{2 * n - 2}",
                          f"e_top_right_half_{2 * n - 1}",
                          f"e_bottom_{2 * n - 1}"]
        edges_to_append_2 = [f"e_top_right_half_{2 * n - 2}",
                          f"e_bottom_between_squares_{2 * n - 2}",
                          f"e_top_left_half_{2 * n - 1}",
                          f"e_right_{2 * n - 1}"]
        matchings_from_smaller_graph_l1r1 = matchings_of_L1R1_graph(n-1)
        matchings_from_smaller_graph_l1r0 = matchings_of_L1R0_graph(n-1)

        # print(f"l1r1: {len(matchings_from_smaller_graph_l1r1)}")
        # print(f"l1r0: {len(matchings_from_smaller_graph_l1r0)}")

        matchings_1 = [m + edges_to_append_1 for m in matchings_from_smaller_graph_l1r1]
        matchings_2 = [m + edges_to_append_2 for m in matchings_from_smaller_graph_l1r0]

        return matchings_1 + matchings_2
    

def matchings_of_L1R0_graph(n):
    if n == 0:
        return matchings_L1R0_zero_case()
    if n == 1:
        return matchings_L1R0_base_case()
    else:
        edges_to_append_1 = [f"e_left_{2 * n}"]
        edges_to_append_2 = [f"e_top_right_half_{2 * n - 2}",
                          f"e_bottom_between_squares_{2 * n - 2}",
                          f"e_top_left_half_{2 * n - 1}",
                          f"e_top_between_squares_{2 * n - 1}",
                          f"e_bottom_between_squares_{2 * n - 1}"]
        matchings_from_smaller_graph_l1r1 = matchings_of_L1R1_graph(n)
        matchings_from_smaller_graph_l1r0 = matchings_of_L1R0_graph(n-1)

        matchings_1 = [m + edges_to_append_1 for m in matchings_from_smaller_graph_l1r1]
        matchings_2 = [m + edges_to_append_2 for m in matchings_from_smaller_graph_l1r0]

        # return matchings_1
        return matchings_1 + matchings_2
    
def matchings_of_L0R1_graph(n):
    if n == 0:
        return matchings_L0R1_zero_case()
    elif n == 1:
        return matchings_L0R1_base_case()
    else:
        edges_to_append_1 = [f"e_top_right_half_{2 * n - 2}",
                          f"e_bottom_between_squares_{2 * n - 2}",
                          f"e_top_left_half_{2 * n - 1}",
                          f"e_right_{2 * n - 1}"]
        
        edges_to_append_2 = [f"e_top_left_half_{2 * n - 2}",
                          f"e_bottom_{2 * n - 2}",
                          f"e_top_between_squares_{2 * n - 2}",
                          f"e_top_right_half_{2 * n - 1}",
                          f"e_bottom_{2 * n - 1}"]
        matchings_from_smaller_graph_l0r0 = matchings_of_L0R0_graph(n-1)
        matchings_from_smaller_graph_l0r1 = matchings_of_L0R1_graph(n-1)

        matchings_1 = [m + edges_to_append_1 for m in matchings_from_smaller_graph_l0r0]
        matchings_2 = [m + edges_to_append_2 for m in matchings_from_smaller_graph_l0r1]

        return matchings_1 + matchings_2
    
def matchings_of_L0R0_graph(n):
    if n == 0:
        return matchings_L0R0_zero_case()
    elif n == 1:
        return matchings_L0R0_base_case()
    else:
        edges_to_append_1 = [f"e_left_{2 * n}"]
        edges_to_append_2 = [f"e_top_right_half_{2 * n - 2}",
                          f"e_bottom_between_squares_{2 * n - 2}",
                          f"e_top_left_half_{2 * n - 1}",
                          f"e_top_between_squares_{2 * n - 1}",
                          f"e_bottom_between_squares_{2 * n - 1}"]
        matchings_from_smaller_graph_l0r1 = matchings_of_L0R1_graph(n)
        matchings_from_smaller_graph_l0r0 = matchings_of_L0R0_graph(n-1)

        matchings_1 = [m + edges_to_append_1 for m in matchings_from_smaller_graph_l0r1]
        matchings_2 = [m + edges_to_append_2 for m in matchings_from_smaller_graph_l0r0]

        return matchings_1 + matchings_2

def matchings_L1R1_zero_case():
    return [[]]

def matchings_L1R1_base_case():
    matchings = []
    matchings.append(["e_top_left_half_0", 
                        "e_bottom_0",
                        "e_top_between_squares_0",
                        "e_top_right_half_1",
                        "e_bottom_1"]
    )
    matchings.append(["e_top_right_half_0", 
                        "e_left_0",
                        "e_bottom_between_squares_0",
                        "e_top_left_half_1",
                        "e_right_1"]
    )
    return matchings

def matchings_L1R0_zero_case():
    return [["e_left_0"]]

def matchings_L1R0_base_case():
    matchings = []
    matchings.append(["e_top_left_half_0", 
                        "e_bottom_0",
                        "e_top_between_squares_0",
                        "e_top_right_half_1",
                        "e_bottom_1",
                        "e_left_2"]
    )
    matchings.append(["e_top_right_half_0", 
                        "e_left_0",
                        "e_bottom_between_squares_0",
                        "e_top_left_half_1",
                        "e_right_1",
                        "e_left_2"]
    )
    matchings.append(["e_top_right_half_0", 
                        "e_left_0",
                        "e_bottom_between_squares_0",
                        "e_top_left_half_1",
                        "e_top_between_squares_1",
                        "e_bottom_between_squares_1"]
    )
    return matchings

def matchings_L0R1_zero_case():
    return [["e_right_-1"]]

def matchings_L0R1_base_case():
    matchings = []
    matchings += [["e_right_-1"] + m for m in matchings_L1R1_base_case()]
    matchings.append([
        "e_top_between_squares_-1",
        "e_bottom_between_squares_-1",
        "e_top_right_half_0",
        "e_bottom_between_squares_0",
        "e_top_left_half_1",
        "e_right_1"
    ])
    return matchings

def matchings_L0R0_zero_case():
    matchings = [["e_right_-1", "e_left_0"],
                 ["e_top_between_squares_-1", "e_bottom_between_squares_-1"]]
    return matchings

def matchings_L0R0_base_case():
    matchings = []
    matchings += [(["e_left_2"] + m) for m in matchings_L0R1_base_case()]
    matchings.append([
        "e_right_-1",
        "e_left_0",
        "e_top_right_half_0",
        "e_bottom_between_squares_0",
        "e_top_left_half_1",
        "e_top_between_squares_1",
        "e_bottom_between_squares_1"
    ])

    matchings.append([
        "e_top_between_squares_-1",
        "e_bottom_between_squares_-1",
        "e_top_right_half_0",
        "e_bottom_between_squares_0",
        "e_top_left_half_1",
        "e_top_between_squares_1",
        "e_bottom_between_squares_1"
    ])

    return matchings

def shift_matching_by_k(matching, k):
    shifted_matching = []

    for e in matching:
        prefix, idx = e.rsplit('_', 1)
        i = int(idx) + k
        shifted_matching.append(f"{prefix}_{i}")

    return shifted_matching

def shift_matchings_by_k(matchings, k):
    shifted_matchings = []

    for m in matchings:
        shifted_matchings.append(shift_matching_by_k(m, k))

    return shifted_matchings

def mod_matching_by_k(matching, k):
    shifted_matching = []

    for e in matching:
        prefix, idx = e.rsplit('_', 1)
        i = int(idx) % k
        shifted_matching.append(f"{prefix}_{i}")

    return shifted_matching

def mod_matchings_by_k(matchings, k):
    shifted_matchings = []

    for m in matchings:
        shifted_matchings.append(mod_matching_by_k(m, k))

    return shifted_matchings


def matchings_of_entropy_graph(n):
    new_edges_if_ll_on_leftmost_pair = ["e_top_left_half_0",
                                    "e_right_0",
                                    "e_top_left_half_1",
                                    "e_bottom_1",
                                    "e_top_between_squares_1",
                                    "e_top_right_half_2",
                                    "e_bottom_2",
                                    f"e_top_right_half_{2 * n - 1}",
                                    f"e_bottom_between_squares_{2 * n - 1}"
    ]
    matchings_l1r0_n_minus_2 = matchings_of_L1R0_graph(n - 2)
    shifted_matchings_l1r0_n_minus_2 = shift_matchings_by_k(matchings_l1r0_n_minus_2, 3)
    matchings_if_ll_on_leftmost_pair = [new_edges_if_ll_on_leftmost_pair + m for m in shifted_matchings_l1r0_n_minus_2]

    new_edges_if_lr_on_leftmost_pair_1 = ["e_top_left_half_0",
                                          "e_top_between_squares_0",
                                          "e_bottom_between_squares_0",
                                          "e_top_right_half_1",
                                          "e_bottom_between_squares_1",
                                          "e_top_left_half_2",
                                          f"e_top_right_half_{2 * n - 1}",
                                          f"e_bottom_between_squares_{2 * n - 1}"]
    
    new_edges_if_lr_on_leftmost_pair_2 = ["e_top_left_half_0",
                                          "e_right_0",
                                          "e_left_1",
                                          "e_top_right_half_1",
                                          "e_bottom_between_squares_1",
                                          "e_top_left_half_2",
                                          f"e_top_right_half_{2 * n - 1}",
                                          f"e_bottom_between_squares_{2 * n - 1}"]
    
    new_edges_if_lr_on_leftmost_pair_3 = ["e_top_left_half_0",
                                          "e_bottom_0",
                                          "e_top_between_squares_0",
                                          "e_bottom_1",
                                          "e_top_right_half_1"
    ]
    matchings_l0r0_n_minus_2 = matchings_of_L0R0_graph(n - 2)
    matchings_l1r1_n_minus_1 = matchings_of_L1R1_graph(n - 1)
    shifted_by_3_matchings_l0r0_n_minus_2 = shift_matchings_by_k(matchings_l0r0_n_minus_2, 3)
    shifted_by_2_matchings_l1r1_n_minus_1 = shift_matchings_by_k(matchings_l1r1_n_minus_1, 2)

    matchings_if_lr_on_leftmost_pair_1 = [new_edges_if_lr_on_leftmost_pair_1 + m for m in shifted_by_3_matchings_l0r0_n_minus_2]
    matchings_if_lr_on_leftmost_pair_2 = [new_edges_if_lr_on_leftmost_pair_2 + m for m in shifted_by_3_matchings_l0r0_n_minus_2]
    matchings_if_lr_on_leftmost_pair_3 = [new_edges_if_lr_on_leftmost_pair_3 + m for m in shifted_by_2_matchings_l1r1_n_minus_1]

    new_edges_if_rl_on_leftmost_pair_1 = ["e_top_right_half_0",
                                        "e_bottom_between_squares_0",
                                        "e_top_left_half_1",
    ]
    new_edges_if_rl_on_leftmost_pair_2 = ["e_top_right_half_0",
                                        "e_bottom_0",
                                        "e_top_left_half_1",
                                        "e_bottom_1",
                                        "e_top_between_squares_1",
                                        "e_top_right_half_2",
                                        "e_bottom_2",
                                        f"e_top_left_half_{2 * n - 1}",
                                        f"e_bottom_{2 * n - 1}",
                                        f"e_top_between_squares_{2 * n - 1}"]
    
    matchings_l0r0_n_minus_1 = matchings_of_L0R0_graph(n - 1)
    matchings_l1r1_n_minus_2 = matchings_of_L1R1_graph(n - 2)

    shifted_by_2_matchings_l0r0_n_minus_1 = mod_matchings_by_k(shift_matchings_by_k(matchings_l0r0_n_minus_1, 2), 2 * n)
    shifted_by_3_matchings_l1r1_n_minus_2 = shift_matchings_by_k(matchings_l1r1_n_minus_2, 3)

    matchings_if_rl_on_leftmost_pair_1 = [new_edges_if_rl_on_leftmost_pair_1 + m for m in shifted_by_2_matchings_l0r0_n_minus_1]
    matchings_if_rl_on_leftmost_pair_2 = [new_edges_if_rl_on_leftmost_pair_2 + m for m in shifted_by_3_matchings_l1r1_n_minus_2]

    new_edges_if_rr_on_leftmost_pair = ["e_top_right_half_0",
                                    "e_bottom_0",
                                    "e_left_1",
                                    "e_top_right_half_1",
                                    "e_bottom_between_squares_1",
                                    "e_top_left_half_2",
                                    f"e_bottom_{2 * n - 1}",
                                    f"e_top_left_half_{2 * n - 1}",
                                    f"e_top_between_squares_{2 * n - 1}"
    ]

    matchings_l0r1_n_minus_2 = matchings_of_L0R1_graph(n - 2)
    shifted_by_3_matchings_l0r1_n_minus_2 = shift_matchings_by_k(matchings_l0r1_n_minus_2, 3)
    matchings_if_rr_on_leftmost_pair = [new_edges_if_rr_on_leftmost_pair + m for m in shifted_by_3_matchings_l0r1_n_minus_2]

    all_matchings = (matchings_if_ll_on_leftmost_pair +
                     matchings_if_lr_on_leftmost_pair_1 + 
                     matchings_if_lr_on_leftmost_pair_2 +
                     matchings_if_lr_on_leftmost_pair_3 +
                     matchings_if_rl_on_leftmost_pair_1 +
                     matchings_if_rl_on_leftmost_pair_2 +
                     matchings_if_rr_on_leftmost_pair
    )

    return all_matchings

# m = matchings_of_L1R0_graph(3)
# print(len(m))

# n = 2

# graph = EntropyGraph(n)
# ms = matchings_of_entropy_graph(n)
# print(f"len of entropy: {len(ms)}")
# for i, m in enumerate(ms):
#     print(m)
#     save_entropy_graph_with_highlighted_edges(graph, m, path=f"output_matchings/entropy_graph_n_{n}_matching_{i}.png")

# exit()

# graph = SquaresGraphL0R0(n)
# ms = matchings_of_L0R0_graph(n)
# print(f"len of l0r0: {len(ms)}")
# for i, m in enumerate(ms):
#     save_squares_graph_with_highlighted_edges(graph, m, path=f"output_matchings_n_3/l0r0_graph_n_{n}_matching_{i}.png")

# graph = SquaresGraphL0R1(n)
# ms = matchings_of_L0R1_graph(n)
# print(f"len of l0r1: {len(ms)}")
# for i, m in enumerate(ms):
#     save_squares_graph_with_highlighted_edges(graph, m, path=f"output_matchings_n_3/l0r1_graph_n_{n}_matching_{i}.png")

# graph = SquaresGraphL1R0(n)
# ms = matchings_of_L1R0_graph(n)
# print(f"len of l1r0: {len(ms)}")
# for i, m in enumerate(ms):
#     save_squares_graph_with_highlighted_edges(graph, m, path=f"output_matchings_n_3/l1r0_graph_n_{n}_matching_{i}.png")

# graph = SquaresGraphL1R1(n)
# ms = matchings_of_L1R1_graph(n)
# print(f"len of l1r1: {len(ms)}")
# for i, m in enumerate(ms):
#     save_squares_graph_with_highlighted_edges(graph, m, path=f"output_matchings_n_3/l1r1_graph_n_{n}_matching_{i}.png")
