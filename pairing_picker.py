"""
Interactive pairing picker for EntropyGraph2.

Usage from Python:

    from entropy_graph import EntropyGraph2
    from pairing_picker import PairingPicker

    g = EntropyGraph2(2)
    picker = PairingPicker(g, outdir="pairings")
    picker.show()

Click edges to toggle black/red.
Click Save Pairing to write selected red edges to pairing_XXX.txt.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Set, Any

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.widgets import Button


class PairingPicker:
    def __init__(
        self,
        graph,
        outdir: str | Path = f"pairings",
        figsize: tuple[float, float] = (10, 4),
        show_names: bool = False,
        title: str = "Pairing picker",
        line_width: float = 3.0,
        vertex_size: float = 20.0,
        pick_radius: float = 6.0,
    ):
        self.graph = graph
        self.outdir = Path(outdir + f"/n_{graph.n}_pairings")
        self.outdir.mkdir(parents=True, exist_ok=True)

        self.figsize = figsize
        self.show_names = show_names
        self.title = title
        self.line_width = line_width
        self.vertex_size = vertex_size
        self.pick_radius = pick_radius

        self.selected_edges: Set[str] = set()
        self.edge_artists: Dict[Any, str] = {}

        self.fig = None
        self.ax = None
        self.save_button = None
        self.clear_button = None

    def show(self):
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.fig.subplots_adjust(bottom=0.18)

        self._draw_edges()
        self._draw_vertices()

        self.ax.set_aspect("equal", adjustable="box")
        self.ax.axis("off")
        self.ax.set_title(self.title, fontsize=14)

        self._add_buttons()

        self.fig.canvas.mpl_connect("pick_event", self._on_pick)

        plt.show()

    def _draw_edges(self):
        for edge in self.graph.edges.values():
            if self._is_horizontal(edge):
                self._draw_horizontal_edge(edge)
            elif self._is_vertical(edge):
                self._draw_vertical_edge(edge)

    def _draw_horizontal_edge(self, edge):
        x1, y1 = edge.left_vertex.x, edge.left_vertex.y
        x2, y2 = edge.right_vertex.x, edge.right_vertex.y

        is_wraparound = x2 < x1

        if is_wraparound:
            rad = 0.18 if edge.is_top_lane else -0.18

            artist = FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-",
                connectionstyle=f"arc3,rad={rad}",
                linewidth=self.line_width,
                color="black",
                mutation_scale=1,
                picker=True,
            )
            self.ax.add_patch(artist)
        else:
            (artist,) = self.ax.plot(
                [x1, x2],
                [y1, y2],
                linewidth=self.line_width,
                color="black",
                picker=self.pick_radius,
            )

        self.edge_artists[artist] = edge.name
        self._maybe_label_edge(edge.name, x1, y1, x2, y2)

    def _draw_vertical_edge(self, edge):
        x1, y1 = edge.up_vertex.x, edge.up_vertex.y
        x2, y2 = edge.down_vertex.x, edge.down_vertex.y

        (artist,) = self.ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=self.line_width,
            color="black",
            picker=self.pick_radius,
        )

        self.edge_artists[artist] = edge.name
        self._maybe_label_edge(edge.name, x1, y1, x2, y2)

    def _draw_vertices(self):
        xs = [v.x for v in self.graph.vertices.values()]
        ys = [v.y for v in self.graph.vertices.values()]

        self.ax.scatter(xs, ys, s=self.vertex_size, zorder=3, color="green")

        if self.show_names:
            for v in self.graph.vertices.values():
                self.ax.text(
                    v.x,
                    v.y + 8,
                    v.name,
                    fontsize=8,
                    ha="center",
                    va="bottom",
                )

    def _maybe_label_edge(self, edge_name, x1, y1, x2, y2):
        if not self.show_names:
            return

        self.ax.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            edge_name,
            fontsize=8,
            ha="center",
            va="center",
        )

    def _add_buttons(self):
        save_ax = self.fig.add_axes([0.70, 0.04, 0.18, 0.07])
        clear_ax = self.fig.add_axes([0.50, 0.04, 0.16, 0.07])

        self.save_button = Button(save_ax, "Save Pairing")
        self.clear_button = Button(clear_ax, "Clear")

        self.save_button.on_clicked(self.save)
        self.clear_button.on_clicked(self.clear)

    def _on_pick(self, event):
        artist = event.artist

        if artist not in self.edge_artists:
            return

        edge_name = self.edge_artists[artist]

        if edge_name in self.selected_edges:
            self.selected_edges.remove(edge_name)
            artist.set_color("black")
        else:
            self.selected_edges.add(edge_name)
            artist.set_color("red")

        self.fig.canvas.draw_idle()

    def clear(self, event=None):
        self.selected_edges.clear()

        for artist in self.edge_artists:
            artist.set_color("black")

        self.fig.canvas.draw_idle()

    def save(self, event=None):
        path = self.next_filename()

        # Preserve visual left-to-right / insertion order from graph.edges.
        ordered_selected = [
            edge_name
            for edge_name in self.graph.edges.keys()
            if edge_name in self.selected_edges
        ]

        with path.open("w", encoding="utf-8") as f:
            for edge_name in ordered_selected:
                f.write(edge_name + "\n")

        print(f"Saved {len(ordered_selected)} edges to {path}")

        self.clear()

    def next_filename(self) -> Path:
        existing = list(self.outdir.glob("pairing_*.txt"))

        ids = []
        for path in existing:
            try:
                ids.append(int(path.stem.split("_")[-1]))
            except ValueError:
                pass

        next_id = max(ids, default=0) + 1
        return self.outdir / f"pairing_{next_id:03d}.txt"

    @staticmethod
    def _is_horizontal(edge) -> bool:
        return hasattr(edge, "left_vertex") and hasattr(edge, "right_vertex")

    @staticmethod
    def _is_vertical(edge) -> bool:
        return hasattr(edge, "up_vertex") and hasattr(edge, "down_vertex")
