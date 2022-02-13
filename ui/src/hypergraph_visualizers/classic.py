import networkx as nx
from hypernetx.drawing.rubber_band import layout_node_link

from ui.src.hypergraph_visualizers import Axes, Hypergraph, \
    HypergraphVisualizer, Coloring, create_color_mapping

import hypernetx as hnx


class Classic(HypergraphVisualizer):
    """
    Классическое представление гиперграфа
    """

    def __init__(self):
        super().__init__()
        self.pos: dict | None = None
        self.facecolors = "black"

    def _draw(
            self,
            axes: Axes,
            hypergraph: Hypergraph,
            coloring: Coloring | None
    ):
        hnx.draw(
            hypergraph,
            ax=axes,
            pos=self.pos,
            edges_kwargs={
                "edgecolors": "gray"
            },
            nodes_kwargs={
                "facecolors": self.facecolors,
            },
            node_labels={
                "fontsize": 10,
            }
        )

    def _calculate_layout(self, hypergraph: Hypergraph, coloring: Coloring | None):
        self.pos = layout_node_link(hypergraph, layout=nx.spring_layout)

    def _calculate_coloring(self, hypergraph: Hypergraph, coloring: Coloring | None):
        if coloring is None:
            self.facecolors = "black"
        else:
            self.facecolors = ["blue" if c == 1 else "black" for c in coloring]

    @property
    def description(self) -> str:
        return "обычное представление графа"
