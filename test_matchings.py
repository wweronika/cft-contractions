from entropy_graph import *
from squares_graph import *
from matchings import matchings_of_entropy_graph, matchings_of_L0R0_graph, matchings_of_L0R1_graph, matchings_of_L1R0_graph, matchings_of_L1R1_graph

def is_valid_perfect_matching(graph, matching):
    """
    Return True iff `matching` is a valid perfect matching on the
    non-leaf vertices of `graph`.

    Assumes graph provides:
    - graph.all_vertices
    - graph.all_edges
    - graph.edge_to_vertices
    - graph.leaf_vertices

    Conditions:
    - every selected edge exists
    - no selected edge touches a leaf vertex
    - every non-leaf vertex is incident to exactly one selected edge
    """
    matching = list(matching)

    all_edges = set(graph.all_edges)
    leaf_vertices = set(graph.leaf_vertices)
    active_vertices = set(graph.all_vertices) - leaf_vertices

    # 1. all selected edges must exist
    for e in matching:
        if e not in all_edges:
            return False

    # 2. count incidences on non-leaf vertices only,
    #    and reject any selected edge touching a leaf
    counts = {v: 0 for v in active_vertices}

    for e in matching:
        u, v = graph.edge_to_vertices[e]

        if u in leaf_vertices or v in leaf_vertices:
            return False

        counts[u] += 1
        counts[v] += 1

    # 3. every non-leaf vertex must appear exactly once
    return all(c == 1 for c in counts.values())

def check_perfect_matching(graph, matching):
    """
    Returns (is_valid, info)

    info contains:
    - invalid_edges
    - edges_touching_leaves
    - overused_vertices
    - unused_vertices
    """
    matching = list(matching)

    all_edges = set(graph.all_edges)
    leaf_vertices = set(graph.leaf_vertices)
    active_vertices = set(graph.all_vertices) - leaf_vertices

    invalid_edges = [e for e in matching if e not in all_edges]
    if invalid_edges:
        return False, {
            "invalid_edges": invalid_edges,
            "edges_touching_leaves": [],
            "overused_vertices": [],
            "unused_vertices": [],
        }

    counts = {v: 0 for v in active_vertices}
    edges_touching_leaves = []

    for e in matching:
        u, v = graph.edge_to_vertices[e]

        if u in leaf_vertices or v in leaf_vertices:
            edges_touching_leaves.append(e)
            continue

        counts[u] += 1
        counts[v] += 1

    if edges_touching_leaves:
        return False, {
            "invalid_edges": [],
            "edges_touching_leaves": edges_touching_leaves,
            "overused_vertices": [],
            "unused_vertices": [],
        }

    overused_vertices = [v for v, c in counts.items() if c > 1]
    unused_vertices = [v for v, c in counts.items() if c == 0]

    is_valid = not overused_vertices and not unused_vertices

    return is_valid, {
        "invalid_edges": [],
        "edges_touching_leaves": [],
        "overused_vertices": overused_vertices,
        "unused_vertices": unused_vertices,
    }

def check_all_perfect_matchings(graph, ms):
    n_ok = 0
    n_bad = 0
    for i, m in enumerate(ms):
        ok, info = check_perfect_matching(graph, m)
        if ok:
            n_ok += 1
        else:
            n_bad += 1
            print(f"i: {i}")
            print(info)
    print(f"OK: {n_ok}, bad: {n_bad}")
    return n_ok, n_bad


n = 10

# graph = SquaresGraphL1R0(n)
# ms = matchings_of_L1R0_graph(n)
# check_all_perfect_matchings(graph, ms)

graph = EntropyGraph(n)
ms = matchings_of_entropy_graph(n)
print("Wick contractions for n=10: ")
check_all_perfect_matchings(graph, ms)
# for matching in ms:

#     ok = is_valid_perfect_matching(graph, matching)

#     ok, info = check_perfect_matching(graph, matching)
#     print(ok, info)
#     input()