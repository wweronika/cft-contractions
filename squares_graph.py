from entropy_graph import Graph
# Squares graph where the leftmost and rightmost ones have a midpoint cut and 
class SquaresGraphL1R1(Graph):
    def __init__(self, n: int):
        edge_to_vertices = self._build(n)
        super().__init__(edge_to_vertices, [], [])
        self.n = n
        self.vertex_to_location = self._embed()
        self.edge_to_location = self._edge_to_location()

    def _build(self, n: int) -> dict[str, tuple[str, str]]:
        # Specific structure of entropy graph for nth Renyi entropy, i.e. 2*n insertions (top edges cut in half)
        edges = {}

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
            if i != 2 * n - 1:
                edges[f"e_top_between_squares_{i}"] = (u, v)

            u = f"v_bottom_right_{i}"
            v = f"v_bottom_left_{(i + 1) % (2 * n)}"
            if i != 2 * n - 1:
                edges[f"e_bottom_between_squares_{i}"] = (u, v)

            u = f"v_top_middle_{i}"

        return edges
    
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
    

class SquaresGraphL1R0(Graph):
    def __init__(self, n: int):
        edge_to_vertices = self._build(n)
        super().__init__(edge_to_vertices, [], [])
        self.n = n
        self.vertex_to_location = self._embed()
        self.edge_to_location = self._edge_to_location()

    def _build(self, n: int) -> dict[str, tuple[str, str]]:
        # Specific structure of entropy graph for nth Renyi entropy, i.e. 2*n insertions (top edges cut in half)
        edges = {}

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
            v = f"v_top_left_{(i + 1)}"
            edges[f"e_top_between_squares_{i}"] = (u, v)

            u = f"v_bottom_right_{i}"
            v = f"v_bottom_left_{(i + 1)}"
            edges[f"e_bottom_between_squares_{i}"] = (u, v)

            if i == 2 * n - 1:
                u = f"v_top_left_{(i + 1)}"
                v = f"v_bottom_left_{(i + 1)}"
                edges[f"e_left_{i+1}"] = (u, v)

        return edges
    
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


class SquaresGraphL0R1(Graph):
    def __init__(self, n: int):
        edge_to_vertices = self._build(n)
        super().__init__(edge_to_vertices, [], [])
        self.n = n
        self.vertex_to_location = self._embed()
        self.edge_to_location = self._edge_to_location()

    def _build(self, n: int) -> dict[str, tuple[str, str]]:
        edges = {}

        # Left dangling boundary segment: mirror of the extra right boundary in L1R0
        u = "v_top_right_-1"
        v = "v_bottom_right_-1"
        edges["e_right_-1"] = (u, v)

        u = "v_top_right_-1"
        v = "v_top_left_0"
        edges["e_top_between_squares_-1"] = (u, v)

        u = "v_bottom_right_-1"
        v = "v_bottom_left_0"
        edges["e_bottom_between_squares_-1"] = (u, v)

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

            if i != 2 * n - 1:
                u = f"v_top_right_{i}"
                v = f"v_top_left_{i + 1}"
                edges[f"e_top_between_squares_{i}"] = (u, v)

                u = f"v_bottom_right_{i}"
                v = f"v_bottom_left_{i + 1}"
                edges[f"e_bottom_between_squares_{i}"] = (u, v)

        return edges

    def _embed(self) -> dict[str, tuple[float, float]]:
        loc = {}

        for v in self.all_vertices:
            parts = v.split("_")
            # format: v_<top/bottom>_<left/middle/right>_<i>

            layer = parts[1]
            horiz = parts[2]
            i = int(parts[3])

            x = 2 * i

            if horiz == "left":
                x_offset = -0.5
            elif horiz == "middle":
                x_offset = 0.0
            else:
                x_offset = 0.5

            if layer == "top":
                y = 1.0
            elif layer == "middle":
                y = 0.5
            else:
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


class SquaresGraphL0R0(Graph):
    def __init__(self, n: int):
        edge_to_vertices = self._build(n)
        super().__init__(edge_to_vertices, [], [])
        self.n = n
        self.vertex_to_location = self._embed()
        self.edge_to_location = self._edge_to_location()

    def _build(self, n: int) -> dict[str, tuple[str, str]]:
        edges = {}

        # Left dangling boundary segment
        u = "v_top_right_-1"
        v = "v_bottom_right_-1"
        edges["e_right_-1"] = (u, v)

        u = "v_top_right_-1"
        v = "v_top_left_0"
        edges["e_top_between_squares_-1"] = (u, v)

        u = "v_bottom_right_-1"
        v = "v_bottom_left_0"
        edges["e_bottom_between_squares_-1"] = (u, v)

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
            v = f"v_top_left_{i + 1}"
            edges[f"e_top_between_squares_{i}"] = (u, v)

            u = f"v_bottom_right_{i}"
            v = f"v_bottom_left_{i + 1}"
            edges[f"e_bottom_between_squares_{i}"] = (u, v)

            if i == 2 * n - 1:
                u = f"v_top_left_{i + 1}"
                v = f"v_bottom_left_{i + 1}"
                edges[f"e_left_{i + 1}"] = (u, v)

        return edges

    def _embed(self) -> dict[str, tuple[float, float]]:
        loc = {}

        for v in self.all_vertices:
            parts = v.split("_")
            # format: v_<top/bottom>_<left/middle/right>_<i>

            layer = parts[1]
            horiz = parts[2]
            i = int(parts[3])

            x = 2 * i

            if horiz == "left":
                x_offset = -0.5
            elif horiz == "middle":
                x_offset = 0.0
            else:
                x_offset = 0.5

            if layer == "top":
                y = 1.0
            elif layer == "middle":
                y = 0.5
            else:
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