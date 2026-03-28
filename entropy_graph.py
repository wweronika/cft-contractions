from copy import deepcopy

def cross2(a, b):
    return a[0]*b[1] - a[1]*b[0]

class Graph:
    def __init__(self, edge_to_vertices: dict[str, tuple[str, str]], leaf_edges: list[str], leaf_vertices: list[str]):
        self.edge_to_vertices = edge_to_vertices
        self.leaf_edges = leaf_edges
        self.leaf_vertices = leaf_vertices
        self.free_loops = 0

        # derive vertices
        verts = set()
        for u, v in edge_to_vertices.values():
            verts.add(u)
            verts.add(v)
        self.all_vertices = list(verts)

        # edges
        self.all_edges = sorted(list(edge_to_vertices.keys()))

        # adjacency
        self.vertex_to_neighbour_vertices = {v: [] for v in self.all_vertices}
        self.vertex_to_neighbour_edges = {v: [] for v in self.all_vertices}

        for e, (u, v) in edge_to_vertices.items():
            self.vertex_to_neighbour_vertices[u].append(v)
            self.vertex_to_neighbour_vertices[v].append(u)

            self.vertex_to_neighbour_edges[u].append(e)
            self.vertex_to_neighbour_edges[v].append(e)

    def delete_edge(self, e: str):
        if e in self.all_edges:
            u, v = self.edge_to_vertices.pop(e)

            self.all_edges.remove(e)

            self.vertex_to_neighbour_edges[u].remove(e)
            self.vertex_to_neighbour_edges[v].remove(e)

            self.vertex_to_neighbour_vertices[u].remove(v)
            self.vertex_to_neighbour_vertices[v].remove(u)


    def delete_vertex(self, v: str):
        # copy since we'll mutate during iteration
        incident_edges = list(self.vertex_to_neighbour_edges[v])
        # print(f"incident_edges of {v}: {incident_edges}")

        for e in incident_edges:
            # print(f"e: {e} in indcident edges, trying to delete")
            self.delete_edge(e)

        self.vertex_to_neighbour_edges.pop(v)
        self.vertex_to_neighbour_vertices.pop(v)

        self.all_vertices.remove(v)

    def add_edge(self, e: str, a: str, b: str):
        self.edge_to_vertices[e] = (a, b)
        self.all_edges.append(e)

        self.vertex_to_neighbour_vertices[a].append(b)
        self.vertex_to_neighbour_vertices[b].append(a)

        self.vertex_to_neighbour_edges[a].append(e)
        self.vertex_to_neighbour_edges[b].append(e)

    def add_edge_or_loop(self, e: str, a: str, b: str):
        if a == b:
            self.free_loops += 1
        else:
            self.add_edge(e, a, b)

    def get_vertices_with_self_loops(self):
        vertices_with_self_loops = []
        for v in self.all_vertices:
            count = 0
            for n in self.vertex_to_neighbour_vertices[v]:
                if n == v:
                    count += 1 
            if count == 2:
                vertices_with_self_loops.append(v)
        return vertices_with_self_loops

    def cut_edge(self, e: str, channel: str):
        # print(f"cutting edge: {e}")
        # print(self.vertex_to_neighbour_edges)
        # print(self.vertex_to_neighbour_vertices)
        v, u = self.edge_to_vertices[e]
        # print(f"u: {u}, v: {v}")
        # print(self.vertex_to_neighbour_edges)

        v_neighbours = [x for x in self.vertex_to_neighbour_vertices[v] if x != u]
        u_neighbours = [x for x in self.vertex_to_neighbour_vertices[u] if x != v]
        # print(v_neighbours, u_neighbours)

        if len(v_neighbours) == 0 and len(u_neighbours) == 0:

            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)

            if channel == "t":
                self.free_loops += 1

        elif len(v_neighbours) == 1 and len(u_neighbours) == 1:
            v1 = v_neighbours[0]
            u1 = u_neighbours[0]

            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)

            self.add_edge(f"{e}_cut_s_0", v1, u1)

            if channel == "t":
                self.free_loops += 1
        else: 
            v1, v2 = v_neighbours
            u1, u2 = u_neighbours

            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)

            if channel == "s":
                self.add_edge_or_loop(f"{e}_cut_s_0", v1, v2)
                self.add_edge_or_loop(f"{e}_cut_s_1", u1, u2)

            elif channel == "t":
                self.add_edge_or_loop(f"{e}_cut_t_0", v1, u1)
                self.add_edge_or_loop(f"{e}_cut_t_1", v2, u2)

            else:
                raise ValueError("channel must be 's' or 't'")

    def cut_edge_4_neighbour_vertices(self, e: str, channel: str):
        v, u, v_neighbours, u_neighbours = self.get_vu_ab_cd_labels_from_edge(e)
        self.cut_edge_4_neighbour_vertices(v, u, v_neighbours, u_neighbours, channel)

    def cut_edge_4_neighbour_vertices(self, e: str, v: str, u: str, v_neighbours: list[str], u_neighbours: list[str], channel: str):

        assert len(v_neighbours) == 2
        assert len(u_neighbours) == 2

        a, b = tuple(v_neighbours)
        c, d = tuple(u_neighbours)

        # print(f"self.all_neighbours_different(u): {self.all_neighbours_different(u)}") 

        # Case 1: 3 lines between 2 vertices, neighbours v: uuu, u: vvv
        if a == u and b == u and c == v and d == v:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.free_loops += 1
            elif channel == "t":
                self.free_loops += 2
        # Case 2: "dumbbell" graph, i.e. loop on left, loop on right, neighbours v: uvv, u: vuu
        elif a == v and b == v and c == u and d == u:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.free_loops += 2
            elif channel == "t":
                self.free_loops += 1
        # Case 3: loop on left, eye on right, neighbours v: uvv, u: vcc               
        elif a == v and b == v and c == d and d != u:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            self.add_edge(f"{e}_cut_0_{channel}", c, c)
            if channel == "s":
                self.free_loops += 1
            elif channel == "t":
                self.free_loops += 0

        # Case 4: eye on left, loop on right, neighbours v: uaa, u: vuu               
        elif a == b and b != v and c == u and d == u:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            self.add_edge(f"{e}_cut_0_{channel}", a, a)
            if channel == "s":
                self.free_loops += 1
            elif channel == "t":
                self.free_loops += 0

        # Case 5: eye on left, eye on right, neighbours v: uaa, u: vcc               
        elif a == b and a != v and c == d and c != u:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, a)
                self.add_edge(f"{e}_cut_1_{channel}", c, c)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, c)
                self.add_edge(f"{e}_cut_1_{channel}", a, c)

        # Case 6: fork on left, fork on right, neighbours v: uab, u: vcd 
        elif self.all_neighbours_different(v) and self.all_neighbours_different(u):
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, b)
                self.add_edge(f"{e}_cut_1_{channel}", c, d)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, c)
                self.add_edge(f"{e}_cut_1_{channel}", b, d)

        # Case 7: fork on left, eye on right, neighbours v: uab, u: vcc 
        elif self.all_neighbours_different(v) and c == d and c != u:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, b)
                self.add_edge(f"{e}_cut_1_{channel}", c, c)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, c)
                self.add_edge(f"{e}_cut_1_{channel}", b, c)

        # Case 8: fork on left, loop on right, neighbours v: uab, u: vuu 
        elif self.all_neighbours_different(v) and c == d and c == u:
            # print("printing self.edge_to_vertices")
            # print(self.edge_to_vertices)
            # self.delete_edge(e)
            # print(f"printing self.edge_to_vertices after deleting edge e: {e}")
            # print(self.edge_to_vertices)
            self.delete_vertex(v)
            self.delete_vertex(u)
            self.delete_edge(e)
            self.add_edge(f"{e}_cut_0_{channel}", a, b)
            if channel == "s":
                self.free_loops += 1
            elif channel == "t":
                self.free_loops += 0

        # Case 9: eye on left, fork on right, neighbours v: uaa, u: vcd 
        elif self.all_neighbours_different(u) and a == b and a != v:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, a)
                self.add_edge(f"{e}_cut_1_{channel}", c, d)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, c)
                self.add_edge(f"{e}_cut_1_{channel}", a, d)

        # Case 10: loop on left, fork on right, neighbours v: uvv, u: vcd
        elif self.all_neighbours_different(u) and a == b and a == v:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            self.add_edge(f"{e}_cut_0_{channel}", c, d)
            if channel == "s":
                self.free_loops += 1
            elif channel == "t":
                self.free_loops += 0

        # Case 11: 2 lines between u and v, other neighbours different, i.e. neighbours v: uua, u: vvc &
        # Case 12: 2 lines between u and v, other neighbours same, i.e. neighbours v: uua, u: vva
        # Both yield same behaviour
        elif self.n_of_edges_between_u_and_v(u, v) == 2: 
            # Pick out the other neighbour vertices, not equal to v or u
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            l = a if a != u else b
            r = c if c != v else d
            self.add_edge(f"{e}_cut_0_{channel}", l, r)
            if channel == "s":
                self.free_loops += 0
            elif channel == "t":
                self.free_loops += 1

        elif a == c and b != d:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, b)
                self.add_edge(f"{e}_cut_1_{channel}", a, d)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, a)
                self.add_edge(f"{e}_cut_1_{channel}", b, d)

        elif a != c and b == d:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, b)
                self.add_edge(f"{e}_cut_1_{channel}", c, b)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, c)
                self.add_edge(f"{e}_cut_1_{channel}", b, b)

        elif a == c and b == d:
            self.delete_edge(e)
            self.delete_vertex(v)
            self.delete_vertex(u)
            if channel == "s":
                self.add_edge(f"{e}_cut_0_{channel}", a, b)
                self.add_edge(f"{e}_cut_1_{channel}", a, b)
            elif channel == "t":
                self.add_edge(f"{e}_cut_0_{channel}", a, a)
                self.add_edge(f"{e}_cut_1_{channel}", b, b)
        else:
            print("CASE NOT HANDLED")

    def get_vu_ab_cd_labels_from_edge(self, e: str):
        v, u = self.edge_to_vertices[e]

        v_neighbours = deepcopy(self.vertex_to_neighbour_vertices[v])
        v_neighbours.remove(u)
        u_neighbours = deepcopy(self.vertex_to_neighbour_vertices[u])
        u_neighbours.remove(v)

        return v, u, v_neighbours, u_neighbours

    def all_neighbours_different(self, v):
        return len(set(self.vertex_to_neighbour_vertices[v])) == len(self.vertex_to_neighbour_vertices[v])
    
    def n_of_edges_between_u_and_v(self, u, v):
        count_u_in_v_neighbours = self.vertex_to_neighbour_vertices[v].count(u)
        count_v_in_u_neighbours = self.vertex_to_neighbour_vertices[u].count(v)

        assert count_u_in_v_neighbours == count_v_in_u_neighbours

        return count_u_in_v_neighbours


class EntropyGraph(Graph):
    def __init__(self, n: int):
        edge_to_vertices, leaf_edges, leaf_vertices = self._build(n)
        super().__init__(edge_to_vertices, leaf_edges, leaf_vertices)
        self.n = n
        self.vertex_to_location = self._embed()
        self.edge_to_location = self._edge_to_location()

    def _build(self, n: int) -> dict[str, tuple[str, str]]:
        # Specific structure of entropy graph for nth Renyi entropy, i.e. 2*n insertions (top edges cut in half)
        edges = {}
        leaf_edges = []
        leaf_vertices = []

        for i in range(2 * n):

            u = f"v_top_left_{i}"
            v = f"v_top_middle_{i}"
            edges[f"e_top_left_half_{i}"] = (u, v)

            u = f"v_top_middle_{i}"
            v = f"v_top_right_{i}"
            edges[f"e_top_right_half_{i}"] = (u, v)

            u = f"v_top_left_{i}"
            v = f"v_bottom_left_{i}"
            edges[f"e_left_{i}"] = (u, v)

            u = f"v_top_right_{i}"
            v = f"v_bottom_right_{i}"
            edges[f"e_right_{i}"] = (u, v)

            u = f"v_bottom_left_{i}"
            v = f"v_bottom_right_{i}"
            edges[f"e_bottom_{i}"] = (u, v)

            u = f"v_top_right_{i}"
            v = f"v_top_left_{(i + 1) % (2 * n)}"
            edges[f"e_top_between_squares_{i}"] = (u, v)

            u = f"v_bottom_right_{i}"
            v = f"v_bottom_left_{(i + 1) % (2 * n)}"
            edges[f"e_bottom_between_squares_{i}"] = (u, v)

            u = f"v_top_middle_{i}"
            v = f"v_middle_middle_{i}"
            edges[f"e_leaf_{i}"] = (u, v)

            leaf_edges.append(f"e_leaf_{i}")
            leaf_vertices.append(f"v_middle_middle_{i}")

        return edges, leaf_edges, leaf_vertices
    
    def cut_edge_4_neighbour_vertices(self, e, channel):
        # print("cutting edge inside entropy graph")
        v, u = self.edge_to_vertices[e]

        v_neighbours = deepcopy(self.vertex_to_neighbour_vertices[v])
        v_neighbours.remove(u)
        u_neighbours = deepcopy(self.vertex_to_neighbour_vertices[u])
        u_neighbours.remove(v)

        # print(f"e: {e}, v: {v}, v_neighbours: {v_neighbours}, u: {u}, u_neighbours: {u_neighbours}")
        assert len(v_neighbours) == 2
        assert len(u_neighbours) == 2

        v, u, a, b, c, d = self.label_4_point_function_vertices(v, u , v_neighbours, u_neighbours)
        # print(f"before cutting v: {v}, u: {u}, a: {a}, b: {b}, c: {c}, d: {d}")
        ab = (a, b)
        cd = (c, d)

        return super().cut_edge_4_neighbour_vertices(e, v, u, ab, cd, channel)

    def _embed(self) -> dict[str, tuple[float, float]]:
        loc = {}

        for v in self.all_vertices:
            parts = v.split("_")
            # format: v_<top/bottom>_<left/middle/right>_<i>

            layer = parts[1]      # top / bottom
            horiz = parts[2]      # left / middle / right
            i = int(parts[3])

            # x-position: strip index
            x = 2*i

            # small horizontal offsets inside each square
            if horiz == "left":
                x_offset = -0.5
            elif horiz == "middle":
                x_offset = 0.0
            else:  # right
                x_offset = 0.5

            # y-position: layer
            if layer == "top":
                y = 1.0
            elif layer == "middle":
                y = 0.5
            else: # bottom 
                y = 0.0

            loc[v] = (x + x_offset, y)

        return loc
    
    def _edge_to_location(self) -> dict[str, tuple[tuple[float, float], tuple[float, float]]]:
        out = {}
        for e, (u, v) in self.edge_to_vertices.items():
            out[e] = (
                self.vertex_to_location[u],
                self.vertex_to_location[v],
            )
        return out
    
    def label_4_point_function_vertices(
        self,
        inner1_label,
        inner2_label,
        neigh_inner1_labels,
        neigh_inner2_labels
    ):
        # Get locations
        inner1 = self.vertex_to_location[inner1_label]
        inner2 = self.vertex_to_location[inner2_label]

        neigh_inner1 = [(lbl, self.vertex_to_location[lbl]) for lbl in neigh_inner1_labels]
        neigh_inner2 = [(lbl, self.vertex_to_location[lbl]) for lbl in neigh_inner2_labels]

        # choose v (left), u (right)
        if inner1[0] <= inner2[0]:
            v_label, u_label = inner1_label, inner2_label
            v, u = inner1, inner2
            neigh_v, neigh_u = neigh_inner1, neigh_inner2
        else:
            v_label, u_label = inner2_label, inner1_label
            v, u = inner2, inner1
            neigh_v, neigh_u = neigh_inner2, neigh_inner1

        # axis vector
        axis = (u[0] - v[0], u[1] - v[1])

        # --- label 1,2 from v ---
        (l0, p0), (l1, p1) = neigh_v

        c0 = cross2(axis, (p0[0] - v[0], p0[1] - v[1]))
        c1 = cross2(axis, (p1[0] - v[0], p1[1] - v[1]))

        if c0 > c1:
            label1, label2 = l0, l1
        else:
            label1, label2 = l1, l0

        # --- label 3,4 from u ---
        (m0, q0), (m1, q1) = neigh_u

        d0 = cross2(axis, (q0[0] - u[0], q0[1] - u[1]))
        d1 = cross2(axis, (q1[0] - u[0], q1[1] - u[1]))

        if d0 > d1:
            label3, label4 = m0, m1
        else:
            label3, label4 = m1, m0

        return v_label, u_label, label1, label2, label3, label4
