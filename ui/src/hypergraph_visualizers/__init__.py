from typing import Type
from hypernetx import Hypergraph
from matplotlib.axes import Axes

from ui.src.hypergraph_visualizers.utils import create_color_mapping
from ui.src.hypergraph_visualizers.hypergraph_visualizer import HypergraphVisualizer, Coloring
from ui.src.hypergraph_visualizers.koenig import Koenig
from ui.src.hypergraph_visualizers.classic import Classic

# список всех доступных способов визуализации гиперграфа
visualizers: list[Type[HypergraphVisualizer]] = [
    Classic,
    Koenig,
]
