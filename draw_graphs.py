import matplotlib.pyplot as plt


def draw_entropy_graph(graph):
    fig, ax = plt.subplots()

    vloc = graph.vertex_to_location
    n = graph.n

    wrap_top = f"e_top_between_squares_{2*n - 1}"
    wrap_bottom = f"e_bottom_between_squares_{2*n - 1}"

    # edges (draw first, lower z-order)
    for e, (u, v) in graph.edge_to_vertices.items():
        x1, y1 = vloc[u]
        x2, y2 = vloc[v]

        if e == wrap_top:
            midx = (x1 + x2) / 2
            ax.plot([x1, midx, x2], [y1, 1.5, y2],
                    color="black", zorder=1)

        elif e == wrap_bottom:
            midx = (x1 + x2) / 2
            ax.plot([x1, midx, x2], [y1, -0.5, y2],
                    color="black", zorder=1)

        else:
            ax.plot([x1, x2], [y1, y2],
                    color="black", zorder=1)

    # vertices (draw after, higher z-order)
    xs = [vloc[v][0] for v in graph.all_vertices]
    ys = [vloc[v][1] for v in graph.all_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="green",
               zorder=2)      # on top
    
    self_loop_vertices = graph.get_vertices_with_self_loops()
    xs = [vloc[v][0] for v in self_loop_vertices]
    ys = [vloc[v][1] for v in self_loop_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="blue",
               zorder=3)      # on top
    
    xs = [vloc[v][0] for v in graph.leaf_vertices]
    ys = [vloc[v][1] for v in graph.leaf_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="red",
               zorder=4)      # on top

    ax.set_aspect("equal")
    ax.axis("off")

    return fig

def draw_entropy_graph_with_highlighted_edges(graph, highlighted_edges):
    fig, ax = plt.subplots()

    vloc = graph.vertex_to_location
    n = graph.n

    wrap_top = f"e_top_between_squares_{2*n - 1}"
    wrap_bottom = f"e_bottom_between_squares_{2*n - 1}"

    # edges (draw first, lower z-order)
    for e, (u, v) in graph.edge_to_vertices.items():
        color = "black"
        if e in highlighted_edges:
            color = "red"
        x1, y1 = vloc[u]
        x2, y2 = vloc[v]

        if e == wrap_top:
            midx = (x1 + x2) / 2
            ax.plot([x1, midx, x2], [y1, 1.5, y2],
                    color=color, zorder=1)

        elif e == wrap_bottom:
            midx = (x1 + x2) / 2
            ax.plot([x1, midx, x2], [y1, -0.5, y2],
                    color=color, zorder=1)

        else:
            ax.plot([x1, x2], [y1, y2],
                    color=color, zorder=1)

    # vertices (draw after, higher z-order)
    xs = [vloc[v][0] for v in graph.all_vertices]
    ys = [vloc[v][1] for v in graph.all_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="green",
               zorder=2)      # on top
    
    xs = [vloc[v][0] for v in graph.leaf_vertices]
    ys = [vloc[v][1] for v in graph.leaf_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="red",
               zorder=3)      # on top

    ax.set_aspect("equal")
    ax.axis("off")

    return fig

def draw_squares_graph(graph):
    fig, ax = plt.subplots()

    vloc = graph.vertex_to_location
    n = graph.n

    # edges (draw first, lower z-order)
    for e, (u, v) in graph.edge_to_vertices.items():
        x1, y1 = vloc[u]
        x2, y2 = vloc[v]


        ax.plot([x1, x2], [y1, y2],
                color="black", zorder=1)

    # vertices (draw after, higher z-order)
    xs = [vloc[v][0] for v in graph.all_vertices]
    ys = [vloc[v][1] for v in graph.all_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="green",
               zorder=2)      # on top
    
    self_loop_vertices = graph.get_vertices_with_self_loops()
    xs = [vloc[v][0] for v in self_loop_vertices]
    ys = [vloc[v][1] for v in self_loop_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="blue",
               zorder=3)      # on top
    
    xs = [vloc[v][0] for v in graph.leaf_vertices]
    ys = [vloc[v][1] for v in graph.leaf_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="red",
               zorder=4)      # on top

    ax.set_aspect("equal")
    ax.axis("off")

    return fig

def draw_squares_graph_with_highlighted_edges(graph, highlighted_edges):
    fig, ax = plt.subplots()

    vloc = graph.vertex_to_location
    n = graph.n

    # edges (draw first, lower z-order)
    for e, (u, v) in graph.edge_to_vertices.items():
        x1, y1 = vloc[u]
        x2, y2 = vloc[v]
        color = "black"
        if e in highlighted_edges:
            color = "red"

        ax.plot([x1, x2], [y1, y2],
                color=color, zorder=1)

    # vertices (draw after, higher z-order)
    xs = [vloc[v][0] for v in graph.all_vertices]
    ys = [vloc[v][1] for v in graph.all_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="green",
               zorder=2)      # on top
    
    self_loop_vertices = graph.get_vertices_with_self_loops()
    xs = [vloc[v][0] for v in self_loop_vertices]
    ys = [vloc[v][1] for v in self_loop_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="blue",
               zorder=3)      # on top
    
    xs = [vloc[v][0] for v in graph.leaf_vertices]
    ys = [vloc[v][1] for v in graph.leaf_vertices]

    ax.scatter(xs, ys,
               s=50,          # larger
               color="red",
               zorder=4)      # on top

    ax.set_aspect("equal")
    ax.axis("off")

    return fig

def save_entropy_graph(graph, path="entropy_graph.png"):
    fig = draw_entropy_graph(graph)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    return path

def show_entropy_graph(graph):
    fig = draw_entropy_graph(graph)
    plt.show()
    return fig

def save_entropy_graph_with_highlighted_edges(graph, edges, path="entropy_graph.png"):
    fig = draw_entropy_graph_with_highlighted_edges(graph, edges)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    return path

def show_entropy_graph_with_highlighted_edges(graph, edges):
    fig = draw_entropy_graph_with_highlighted_edges(graph, edges)
    plt.show()
    return fig

def save_squares_graph(graph, path="squares_graph.png"):
    fig = draw_squares_graph(graph)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    return path

def save_squares_graph_with_highlighted_edges(graph, edges, path="entropy_graph.png"):
    fig = draw_squares_graph_with_highlighted_edges(graph, edges)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    return path