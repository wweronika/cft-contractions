import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from itertools import product
import os

class HorizontalEdge:
    def __init__(self, name, u, v, is_top_lane):
        self.name = name
        self.left_vertex = u
        self.right_vertex = v
        self.is_top_lane = is_top_lane

class VerticalEdge:
    def __init__(self, name, u, v):
        self.name = name
        self.up_vertex = u
        self.down_vertex = v

class Vertex:
    def __init__(self, name, x, y, lane):
        self.name = name
        self.x = x
        self.y = y
        self.adjacent_edges = {}
        self.neighbour_vertices = {}
        self.lane = lane

    # def __init__(self, lv, le, rv, re, tv, te, bv, be, name, x, y):
    #     self.left_neighbour_vertex = lv
    #     self.left_edge = le
    #     self.right_neighbour_vertex = rv
    #     self.right_edge = rv
    #     self.top_neighbour_vertex = tv
    #     self.top_edge = te
    #     self.bottom_neighbour_vertex = bv
    #     self.bottom_edge = be
    #     self.name = name
    #     self.x = x
    #     self.y = y



class EntropyGraph2:
    def __init__(self, n):
        self.n = n
        self.edges = {}
        self.vertices = {}
        self._build(n)
        self.top_offset = 20
        self.bottom_offset = 20
        self.right_offset = 20

    def cut_edge_top_t_channel(self, edge_name):
        edge = self.edges[edge_name]
        u = edge.left_vertex
        v = edge.right_vertex
        a = u.neighbour_vertices["left"]
        b = u.neighbour_vertices["down"]
        c = v.neighbour_vertices["down"]
        d = v.neighbour_vertices["right"]


        edl = u.adjacent_edges["down"]
        edr = v.adjacent_edges["down"]

        self.delete_vertical_edge(edl.name)
        self.delete_vertical_edge(edr.name)

        u2_name = u.name + "_below"
        v2_name = v.name + "_below"
        self.add_vertex_below_vertex(u, u2_name)
        self.add_vertex_below_vertex(v, v2_name)
        # self.top_offset -= 4

        self.connect(u2_name, b.name, "down", edl.name + "_cut")
        self.connect(v2_name, c.name, "down", edr.name + "_cut")
        self.connect(u2_name, v2_name, "right", edge_name + "_cut")


    def cut_edge_bottom_t_channel(self, edge_name):
        edge = self.edges[edge_name]
        u = edge.left_vertex
        v = edge.right_vertex
        a = u.neighbour_vertices["left"]
        b = u.neighbour_vertices["up"]
        c = v.neighbour_vertices["up"]
        d = v.neighbour_vertices["right"]


        eul = u.adjacent_edges["up"]
        eur = v.adjacent_edges["up"]

        self.delete_vertical_edge(eul.name)
        self.delete_vertical_edge(eur.name)

        u2_name = u.name + "_above"
        v2_name = v.name + "_above"
        self.add_vertex_above_vertex(u, u2_name)
        self.add_vertex_above_vertex(v, v2_name)
        # self.bottom_offset -= 4

        self.connect(u2_name, b.name, "up", eul.name + "_cut")
        self.connect(v2_name, c.name, "up", eur.name + "_cut")
        self.connect(u2_name, v2_name, "right", edge_name + "_cut")

    def cut_edge_vertical_t_channel(self, edge_name):
        edge = self.edges[edge_name]
        u = edge.up_vertex
        v = edge.down_vertex
        a = u.neighbour_vertices["left"]
        b = u.neighbour_vertices["right"]
        c = v.neighbour_vertices["left"]
        d = v.neighbour_vertices["right"]


        eur = u.adjacent_edges["right"]
        edr = v.adjacent_edges["right"]

        self.delete_horizontal_edge(eur.name)
        self.delete_horizontal_edge(edr.name)

        u2_name = u.name + "_rightshift"
        v2_name = v.name + "_rightshift"
        self.add_vertex_right_of_vertex(u, u2_name)
        self.add_vertex_right_of_vertex(v, v2_name)
        # self.bottom_offset -= 4

        self.connect(u2_name, b.name, "right", eur.name + "_cut")
        self.connect(v2_name, d.name, "right", edr.name + "_cut")
        self.connect(u2_name, v2_name, "down", edge_name + "_cut")

    def cut_edge_top_s_channel(self, edge_name):
        self.delete_horizontal_edge(edge_name)

    def cut_edge_bottom_s_channel(self, edge_name):
        self.delete_horizontal_edge(edge_name)

    def cut_edge_vertical_s_channel(self, edge_name):
        self.delete_vertical_edge(edge_name)

    def cut_edge(self, edge_name, channel):
        edge = self.edges[edge_name]
        if isinstance(edge, HorizontalEdge):
            if edge.is_top_lane:
                if channel == "s":
                    self.cut_edge_top_s_channel(edge_name)
                elif channel == "t":
                    self.cut_edge_top_t_channel(edge_name)
            else:
                if channel == "s":
                    self.cut_edge_bottom_s_channel(edge_name)
                elif channel == "t":
                    self.cut_edge_bottom_t_channel(edge_name)
        elif isinstance(edge, VerticalEdge):
            if channel == "s":
                self.cut_edge_vertical_s_channel(edge_name)
            elif channel == "t":
                    self.cut_edge_vertical_t_channel(edge_name)    

    def cut_edges(self, edge_names, channels):
        if len(channels) != len(edge_names):
            return
        for i in range(len(edge_names)):
            self.cut_edge(edge_names[i], channels[i])

    def add_vertex(self, name, x, y, lane):
        new_vertex = Vertex(name, x, y, lane) 
        self.vertices[name] = new_vertex

    def add_vertex_below_vertex(self, v, v2_name):
        self.add_vertex(v2_name, v.x, v.y-self.bottom_offset, v.lane)

    def add_vertex_above_vertex(self, v, v2_name):
        self.add_vertex(v2_name, v.x, v.y+self.top_offset, v.lane)

    def add_vertex_right_of_vertex(self, v, v2_name):
        self.add_vertex(v2_name, v.x+self.right_offset, v.y, v.lane)

    def delete_horizontal_edge(self, edge_name):
        edge = self.edges[edge_name]
        del edge.left_vertex.adjacent_edges["right"]
        del edge.left_vertex.neighbour_vertices["right"]
        del edge.right_vertex.adjacent_edges["left"]
        del edge.right_vertex.neighbour_vertices["left"]

        del self.edges[edge_name]

    def delete_vertical_edge(self, edge_name):
        edge = self.edges[edge_name]
        del edge.up_vertex.adjacent_edges["down"]
        del edge.up_vertex.neighbour_vertices["down"]
        del edge.down_vertex.adjacent_edges["up"]
        del edge.down_vertex.neighbour_vertices["up"]

        del self.edges[edge_name]

    def connect(self, u_name, v_name, direction, edge_name):
        opposite = {"left" : "right", "right" : "left", "up" : "down", "down" : "up"}
        new_edge = None

        u = self.vertices[u_name]
        v = self.vertices[v_name]

        if direction == "left" or direction == "right":
            if u.lane != v.lane or u.lane == "middle" or v.lane == "middle":
                return
            else:
                is_top_lane = (u.lane == "top")
                new_edge = HorizontalEdge(edge_name, u, v, is_top_lane)

        elif direction == "up":
            new_edge = VerticalEdge(edge_name, v, u)

        elif direction == "down":
            new_edge = VerticalEdge(edge_name, u, v)
        
        opposite_direction = opposite[direction]
        u.adjacent_edges[direction] = new_edge
        u.neighbour_vertices[direction] = v
        v.adjacent_edges[opposite_direction] = new_edge
        v.neighbour_vertices[opposite_direction] = u

        self.edges[edge_name] = new_edge

    def _build(self, n):
        for i in range(2 * n):
            self.add_vertex(f"v_top_left_{i}", x=i*200, y=100, lane="top")
            self.add_vertex(f"v_top_middle_{i}", x=i*200+50, y=100, lane="top")
            self.add_vertex(f"v_top_right_{i}", x=i*200+100, y=100, lane="top")

            self.add_vertex(f"v_bottom_left_{i}", x=i*200, y=0, lane="bottom")
            self.add_vertex(f"v_bottom_right_{i}", x=i*200+100, y=0, lane="bottom")

            self.add_vertex(f"v_centre_of_square_{i}", x=i*200+50, y=50, lane="middle")

        for i in range(2 * n):
            self.connect(f"v_top_left_{i}", f"v_top_middle_{i}", "right", f"e_top_left_half_{i}")
            self.connect(f"v_top_middle_{i}", f"v_top_right_{i}", "right", f"e_top_right_half_{i}")
            self.connect(f"v_top_right_{i}", f"v_top_left_{(i+1) % (2*n)}", "right", f"e_top_between_squares_{i}")

            self.connect(f"v_bottom_left_{i}", f"v_bottom_right_{i}", "right", f"e_bottom_{i}")
            self.connect(f"v_bottom_right_{i}", f"v_bottom_left_{(i+1) % (2*n)}", "right", f"e_bottom_between_squares_{i}")

            self.connect(f"v_top_right_{i}", f"v_bottom_right_{i}", "down", f"e_right_{i}")
            self.connect(f"v_top_left_{i}", f"v_bottom_left_{i}", "down", f"e_left_{i}")

            self.connect(f"v_top_middle_{i}", f"v_centre_of_square_{i}", "down", f"e_leaf_{i}")

    def count_components(self):
        """
        Returns:
            {
                "line_components": int,
                "loop_components": int,
                "other_components": int,
                "components": list[set[str]]
            }

        A line-like component is connected and has exactly two degree-1 vertices.
        A loop component is connected and every vertex has degree 2.
        """

        visited = set()
        components = []

        def degree(v):
            return len(v.neighbour_vertices)

        for v in self.vertices.values():
            if v.name in visited:
                continue

            # Ignore isolated deleted/unused vertices if any.
            if degree(v) == 0:
                continue

            stack = [v]
            comp = set()
            visited.add(v.name)

            while stack:
                cur = stack.pop()
                comp.add(cur.name)

                for nb in cur.neighbour_vertices.values():
                    if nb.name not in visited:
                        visited.add(nb.name)
                        stack.append(nb)

            components.append(comp)

        line_components = 0
        loop_components = 0
        other_components = 0

        for comp in components:
            degrees = [degree(self.vertices[name]) for name in comp]

            n_deg_1 = sum(d == 1 for d in degrees)
            all_deg_2 = all(d == 2 for d in degrees)

            if all_deg_2:
                loop_components += 1
            elif n_deg_1 == 2 and all(d in {1, 2} for d in degrees):
                line_components += 1
            else:
                other_components += 1

        return {
            "n_lines": line_components,
            "n_loops": loop_components,
            "n_other": other_components,
            "components": components,
        }

    def draw(self, ax=None, show_names=True, figsize=(10, 4), title="final_graph", outdir="out"):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        # Draw edges
        for edge in self.edges.values():
            if isinstance(edge, HorizontalEdge):
                x1, y1 = edge.left_vertex.x, edge.left_vertex.y
                x2, y2 = edge.right_vertex.x, edge.right_vertex.y

                is_wraparound = x2 < x1
                if edge.is_top_lane:
                    angle = "0.18"
                else:
                    angle = "-0.18"
                if is_wraparound:
                    arc = FancyArrowPatch(
                        (x1, y1),
                        (x2, y2),
                        arrowstyle="-",
                        connectionstyle=f"arc3,rad={angle}",
                        linewidth=2,
                        mutation_scale=1,
                    )
                    ax.add_patch(arc)
                else:
                    ax.plot([x1, x2], [y1, y2], linewidth=2, color="black")
            elif isinstance(edge, VerticalEdge):
                x1, y1 = edge.up_vertex.x, edge.up_vertex.y
                x2, y2 = edge.down_vertex.x, edge.down_vertex.y
                ax.plot([x1, x2], [y1, y2], linewidth=2, color="black")
            else:
                continue

            if show_names:
                ax.text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    edge.name,
                    fontsize=8,
                    ha="center",
                    va="center",
                )

        # Draw vertices
        xs = [v.x for v in self.vertices.values()]
        ys = [v.y for v in self.vertices.values()]

        ax.scatter(xs, ys, s=20, zorder=3, color="green")

        if show_names:
            for v in self.vertices.values():
                ax.text(
                    v.x,
                    v.y + 8,
                    v.name,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                )

        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=14)
        n_components = self.count_components()
        subtitle = f"n loops: {n_components["n_loops"]}, n_lines: {n_components["n_lines"]}"
        print(f"n loops: {n_components["n_loops"]}, channels: {title}")
        ax.text(
            0.5,  0.94,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=10
        )

        # plt.show()
        plt.savefig(f'{outdir}/{title}.png')
        plt.close()
        return fig, ax
    
    def draw_with_highlighted_edges(self, highlighted_edges, ax=None, show_names=True, figsize=(10, 4), title="graph_before_cutting", outdir="out"):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        # Draw edges
        color = "black"
        for edge in self.edges.values():
            color = "black"
            if edge.name in highlighted_edges:
                color = "red"
            if isinstance(edge, HorizontalEdge):
                x1, y1 = edge.left_vertex.x, edge.left_vertex.y
                x2, y2 = edge.right_vertex.x, edge.right_vertex.y

                is_wraparound = x2 < x1
                if edge.is_top_lane:
                    angle = "0.18"
                else:
                    angle = "-0.18"
                if is_wraparound:
                    arc = FancyArrowPatch(
                        (x1, y1),
                        (x2, y2),
                        arrowstyle="-",
                        connectionstyle=f"arc3,rad={angle}",
                        linewidth=2,
                        mutation_scale=1,
                        color=color
                    )
                    ax.add_patch(arc)
                else:
                    ax.plot([x1, x2], [y1, y2], linewidth=2, color=color)
            elif isinstance(edge, VerticalEdge):
                x1, y1 = edge.up_vertex.x, edge.up_vertex.y
                x2, y2 = edge.down_vertex.x, edge.down_vertex.y
                ax.plot([x1, x2], [y1, y2], linewidth=2, color=color)
            else:
                continue

            if show_names:
                ax.text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    edge.name,
                    fontsize=8,
                    ha="center",
                    va="center",
                )

        # Draw vertices
        xs = [v.x for v in self.vertices.values()]
        ys = [v.y for v in self.vertices.values()]

        ax.scatter(xs, ys, s=20, zorder=3, color="green")

        if show_names:
            for v in self.vertices.values():
                ax.text(
                    v.x,
                    v.y + 8,
                    v.name,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                )

        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=14)
        n_components = self.count_components()
        subtitle = f"n loops: {n_components["n_loops"]}, n_lines: {n_components["n_lines"]}"
        print(f"n loops: {n_components["n_loops"]}, channels: {title}")
        ax.text(
            0.5,  0.94,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=10
        )

        # plt.show()
        plt.savefig(f'{outdir}/{title}.png')
        plt.close()
        return fig, ax

    def get_edges_to_cut_across_1(n):
        edges_to_cut = []
        for i in range(n):
            edges_to_cut.append(f"e_top_left_half_{2 * i}")
            edges_to_cut.append(f"e_top_between_squares_{2 * i}")
            edges_to_cut.append(f"e_top_right_half_{(2 * i + 1) % (2 * n)}")
            edges_to_cut.append(f"e_bottom_between_squares_{2 * i}")
            edges_to_cut.append(f"e_bottom_between_squares_{(2 * i + 1) % (2 * n)}")
        return edges_to_cut
    
    def get_edges_to_cut_across_2(n):
        edges_to_cut = []
        for i in range(n):
            edges_to_cut.append(f"e_top_left_half_{2 * i}")
            edges_to_cut.append(f"e_top_between_squares_{2 * i}")
            edges_to_cut.append(f"e_top_right_half_{2 * i + 1}")
            edges_to_cut.append(f"e_bottom_{2 * i}")
            edges_to_cut.append(f"e_bottom_{2 * i + 1}")
        return edges_to_cut
    
    def get_edges_to_cut_within_1(n):
        edges_to_cut = []
        for i in range(n):
            edges_to_cut.append(f"e_top_left_half_{2 * i}")
            edges_to_cut.append(f"e_top_right_half_{2 * i + 1}")
            edges_to_cut.append(f"e_right_{2 * i}")
            edges_to_cut.append(f"e_left_{2 * i + 1}")
            edges_to_cut.append(f"e_bottom_between_squares_{2 * i + 1}")
        return edges_to_cut
    
    # Works for even only
    def get_edges_to_cut_within_2(n):
        edges_to_cut = []
        for i in range(n // 2):
            edges_to_cut.append(f"e_top_left_half_{4 * i}")
            edges_to_cut.append(f"e_top_right_half_{4 * i + 1}")
            edges_to_cut.append(f"e_top_between_squares_{4 * i}")
            edges_to_cut.append(f"e_bottom_{4 * i}")
            edges_to_cut.append(f"e_bottom_{4 * i + 1}")

            edges_to_cut.append(f"e_top_right_half_{4 * i + 2}")
            edges_to_cut.append(f"e_top_left_half_{4 * i + 3}")
            edges_to_cut.append(f"e_left_{4 * i + 2}")
            edges_to_cut.append(f"e_right_{4 * i + 3}")
            edges_to_cut.append(f"e_bottom_between_squares_{4 * i + 2}")
        return edges_to_cut



channels = ["s", "t"]

# outdir_across = "output_new_n_1_across_wavefunctions"
# edges_to_cut_across = ["e_top_left_half_0",
#             "e_top_right_half_1",
#             "e_top_between_squares_0",
#             "e_bottom_between_squares_0",
#             "e_bottom_between_squares_1"]
# for channel_order in product(channels, repeat=len(edges_to_cut_across)):
#     g = EntropyGraph2(1)
#     g.cut_edges(edges_to_cut_across, channel_order)
#     g.draw(show_names=False, title=''.join(channel_order), outdir=outdir_across)

# outdir_within = "output_new_n_1_within_wavefunctions"
# edges_to_cut_within = ["e_top_left_half_0",
#             "e_top_right_half_1",
#             "e_right_0",
#             "e_left_1",
#             "e_bottom_between_squares_1"]
# for channel_order in product(channels, repeat=len(edges_to_cut_within)):
#     g = EntropyGraph2(1)
#     g.cut_edges(edges_to_cut_within, channel_order)
#     g.draw(show_names=False, title=''.join(channel_order), outdir=outdir_within)

n = 1

# outdir = f"output_new_n_{n}_across_wavefunctions_1"
# os.makedirs(outdir, exist_ok=True)
# edges_to_cut = EntropyGraph2.get_edges_to_cut_across_1(n)

outdir = f"output_new_n_{n}_within_wavefunctions_1"
os.makedirs(outdir, exist_ok=True)
edges_to_cut = EntropyGraph2.get_edges_to_cut_within_1(n)

# outdir = f"output_new_n_{n}_across_wavefunctions_2"
# os.makedirs(outdir, exist_ok=True)
# edges_to_cut = EntropyGraph2.get_edges_to_cut_across_2(n)

# outdir = f"output_new_n_{n}_within_wavefunctions_2"
# os.makedirs(outdir, exist_ok=True)
# edges_to_cut = EntropyGraph2.get_edges_to_cut_within_2(n)

g = EntropyGraph2(n)
g.draw_with_highlighted_edges(edges_to_cut, show_names=False, title=f'n_{2}_before_cutting', outdir=outdir)
for channel_order in product(channels, repeat=len(edges_to_cut)):
    g = EntropyGraph2(n)
    g.cut_edges(edges_to_cut, channel_order)
    g.draw(show_names=False, title=''.join(channel_order), outdir=outdir)