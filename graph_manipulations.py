from entropy_graph import EntropyGraph
from draw_graphs import *
from itertools import product
from copy import deepcopy
import matplotlib.pyplot as plt
import os

def test_all_orderings(graph, inner1, inner2, neigh1, neigh2):
    """
    Enumerate all 8 valid combinations of:
      - swapping inner1/inner2 together with their attached neighbor lists
      - swapping order inside neigh1
      - swapping order inside neigh2
    """
    results = []

    for swap_inner, swap_n1, swap_n2 in product([False, True], repeat=3):

        if not swap_inner:
            i1, i2 = inner1, inner2
            g1, g2 = neigh1[:], neigh2[:]
        else:
            i1, i2 = inner2, inner1
            g1, g2 = neigh2[:], neigh1[:]   # important

        if swap_n1:
            g1 = g1[::-1]
        if swap_n2:
            g2 = g2[::-1]

        output = graph.label_4_point_function_vertices(i1, i2, g1, g2)

        results.append({
            "swap_inner": swap_inner,
            "swap_neigh1": swap_n1,
            "swap_neigh2": swap_n2,
            "input": (i1, i2, g1, g2),
            "output": output,
        })

    return results

def check_all_outputs_same(results):
    outputs = [tuple(r["output"]) for r in results]
    first = outputs[0]

    all_same = all(out == first for out in outputs)

    if all_same:
        print("All outputs are the same.")
        # print("Output:", first)
    else:
        print("Not all outputs are the same.")
        print("\nDistinct outputs:")
        for out in sorted(set(outputs)):
            print(out)

        print("\nCases:")
        for i, r in enumerate(results):
            same = tuple(r["output"]) == first
            print(
                f"{i}: same={same}, "
                f"inner_swap={r['swap_inner']}, "
                f"n1_swap={r['swap_neigh1']}, "
                f"n2_swap={r['swap_neigh2']}, "
                f"output={r['output']}"
            )

    return all_same

def cut_edges_in_all_channels(graph, edges_to_cut):
    channels = ["s", "t"]

    for channel_order in product(channels, repeat=len(edges_to_cut)):
        print(f"attempting channels: {channel_order}")
        graph_tmp = deepcopy(graph)
        channel_string = ''.join(channel_order)

        save_entropy_graph_with_highlighted_edges(
            graph_tmp,
            edges_to_cut,
            path="entropy_graph_before_cutting.png",
        )

        for edge, channel in zip(edges_to_cut, channel_order):
            graph_tmp.cut_edge_4_neighbour_vertices(edge, channel)

        save_entropy_graph(graph_tmp, path=f"output/test2_entropy_graph_{channel_string}.png")
        plt.close()
        print(f"channels: {channel_string}, n loops: {graph_tmp.free_loops}")

def cut_edges_in_one_channel(graph, edges_to_cut, channel_order):

    print(f"attempting single channel combination: {channel_order}")
    graph_tmp = deepcopy(graph)

    folder = f"output/{channel_order}_full_path/"
    path_before = f"output/{channel_order}_full_path/entropy_graph_before_cutting.png"

    save_entropy_graph_with_highlighted_edges(
        graph_tmp,
        edges_to_cut,
        path=path_before,
    )

    for i, (edge, channel) in enumerate(zip(edges_to_cut, channel_order)):
        graph_tmp.cut_edge_4_neighbour_vertices(edge, channel)
        path = f"output/{channel_order}_full_path/entropy_graph_{channel_order[:(i+1)]}.png"
        save_entropy_graph(graph_tmp, path=path)

    plt.close()
    print(f"channels: {channel_order}, n loops: {graph_tmp.free_loops}")



