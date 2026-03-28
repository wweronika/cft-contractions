from entropy_graph import EntropyGraph
from squares_graph import SquaresGraphL1R1, SquaresGraphL1R0, SquaresGraphL0R1, SquaresGraphL0R0
from draw_graphs import *
from graph_manipulations import cut_edges_in_all_channels, cut_edges_in_one_channel


n = 1
graph = EntropyGraph(n)

# print(graph.edge_to_vertices)
# save_entropy_graph(graph, path=f"output_before_cut/entropy_graph_before_cutting_n_{n}.png")
edges_to_cut = ["e_top_left_half_0", 
                "e_top_between_squares_0",
                "e_bottom_between_squares_0",
                "e_top_right_half_1",
                "e_bottom_between_squares_1"
]

# channels = "sssst"
channels = "sssts"

# graph.cut_edge("e_top_left_half_0", channel="s")
# save_entropy_graph_with_highlighted_edges(graph, edges_to_cut, path="output_before_cut/entropy_graph_before_cut_n_{n}_highlighted.png")

# for i in range(len(channels)):
#     print(f"ITERATION {i}")
#     graph.cut_edge_4_neighbour_vertices(edges_to_cut[i], channels[i])

#     save_entropy_graph(graph, path=f"test_{channels[:i+1]}.png")
#     print(graph.free_loops)
#     print(graph.all_edges)
#     # print(graph.vertex_to_neighbour_vertices["v_bottom_right_0"])
#     # print(graph.vertex_to_neighbour_edges["v_bottom_right_0"])
#     input()

# cut_edges_in_all_channels(graph, edges_to_cut)
cut_edges_in_one_channel(graph, edges_to_cut, channels)
# graph = SquaresGraphL0R0(2)
# save_squares_graph(graph)
    

