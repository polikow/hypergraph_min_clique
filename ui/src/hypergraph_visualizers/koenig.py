from itertools import chain

import networkx as nx
import numpy as np

from networkx.drawing.layout import rescale_layout

from ui.src.hypergraph_visualizers import Axes, Hypergraph, \
    HypergraphVisualizer, Coloring, create_color_mapping


class Koenig(HypergraphVisualizer):
    """
    Кенигово представление гиперграфа

    Гиперграф представляется в виде двудольного графа, в котором
    первая доля вершин состоит из исходных вершин гиперграфа, а
    вторая - из гиперребер гиперграфа.

    Особенности реализации:
        1) Верхний ряд представляет собой ребра гиперграфа
        2) Нижний ряд - исходные вершины гиперграфа
    """

    def __init__(self):
        super().__init__()
        self.graph: nx.Graph | None = None
        self.nodes: list[str] | None = None
        self.edge_nodes: list[str] | None = None
        self.pos: dict | None = None

        self.node_color = "black"

    def _draw(
            self,
            axes: Axes,
            hypergraph: Hypergraph,
            coloring: Coloring | None
    ):
        axes.set_axis_off()
        generic_kwargs = dict(
            G=self.graph,
            pos=self.pos,
            ax=axes
        )
        nx.draw_networkx_nodes(
            node_color=self.node_color,
            **generic_kwargs
        )
        nx.draw_networkx_edges(
            **generic_kwargs
        )
        Koenig.draw_labels(axes, hypergraph, self.pos)

    @staticmethod
    def draw_labels(axes: Axes, hypergraph: Hypergraph, pos: dict):
        for node, (x, y) in pos.items():
            axes.text(
                x,
                y + (-0.1 if node in hypergraph.nodes else 0.1),
                node,
                size=12,
                color="k",
                family="sans-serif",
                weight="normal",
                alpha=None,
                horizontalalignment="center",
                verticalalignment="center",
                transform=axes.transData,
                bbox=None,
                clip_on=True,
            )

    def _calculate_layout(self, hypergraph: Hypergraph, coloring: Coloring | None):
        nodes = list(hypergraph.nodes)
        edge_nodes = list(hypergraph.edges)

        graph: nx.Graph = nx.Graph()
        graph.add_nodes_from(nodes, bipartite=0)
        graph.add_nodes_from(edge_nodes, bipartite=1)
        for edge in hypergraph.incidence_dict.keys():
            for node in hypergraph.incidence_dict[edge]:
                graph.add_edge(edge, node)

        pos = Koenig.bipartite_layout(
            top=edge_nodes,
            bottom=nodes,
        )

        self.graph = graph
        self.nodes = nodes
        self.edge_nodes = edge_nodes
        self.pos = pos
        self.node_color = "black"

    def _calculate_coloring(self, hypergraph: Hypergraph, coloring: Coloring | None):
        if coloring is None:
            self.node_color = "black"
        else:
            self.node_color = [
                *["blue" if c == 1 else "black" for c in coloring],
                *["black" for _ in range(len(self.graph.nodes) - len(coloring))]
            ]

    @staticmethod
    def bipartite_layout(top, bottom, scale=1, aspect_ratio=4 / 3):
        top, bottom = bottom, top
        height = 1
        width = aspect_ratio * height
        offset = (width / 2, height / 2)

        left_xs = np.repeat(0, len(top))
        right_xs = np.repeat(width, len(bottom))
        left_ys = np.linspace(0, height, len(top))
        right_ys = np.linspace(0, height, len(bottom))

        top_pos = np.column_stack([left_xs, left_ys]) - offset
        bottom_pos = np.column_stack([right_xs, right_ys]) - offset

        pos = np.concatenate([top_pos, bottom_pos])
        pos = rescale_layout(pos, scale=scale) + np.zeros(2)
        pos = np.flip(pos, 1)
        pos = dict(zip(chain(top, bottom), pos))
        return pos

    @property
    def description(self) -> str:
        return "Кёнигово представление гиперграфа"
