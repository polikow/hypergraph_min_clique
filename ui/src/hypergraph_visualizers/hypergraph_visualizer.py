from abc import ABC, abstractmethod

from hypernetx import Hypergraph
from matplotlib.axes import Axes

Coloring = tuple[int, ...]


class HypergraphVisualizer(ABC):
    """
    Базовый для всех способов отрисовки гиперграфа класс
    """

    def __init__(self):
        # последний отрисованный гиперграф и его цвета
        self.hypergraph: Hypergraph | None = None
        self.coloring: Coloring | None = None

    def draw(
            self,
            axes: Axes,
            hypergraph: Hypergraph,
            coloring: Coloring | None
    ):
        """Отрисовывает гиперграф с заданным сочетанием"""
        self._prepare_to_draw(hypergraph, coloring)
        self._draw(axes, hypergraph, coloring)

        self.hypergraph = hypergraph
        self.coloring = coloring

    def draw_ignore_hash(
            self,
            axes: Axes,
            hypergraph: Hypergraph,
            coloring: Coloring | None
    ):
        self._calculate_layout(hypergraph, coloring)
        self._calculate_coloring(hypergraph, coloring)
        self._draw(axes, hypergraph, coloring)

        self.hypergraph = hypergraph
        self.coloring = coloring

    def _prepare_to_draw(self, hypergraph: Hypergraph, coloring: Coloring | None):
        """
        Подготовка к отрисовке: вычисление разметки графа и его раскраски.

        Разметка не будет заново вычислена, если рисуется один и тот же гиперграф.
        """
        if hash(hypergraph) != hash(self.hypergraph):
            self._calculate_layout(hypergraph, coloring)
            self.coloring = None

        if coloring != self.coloring or coloring is None:
            self._calculate_coloring(hypergraph, coloring)

    @abstractmethod
    def _calculate_layout(self, hypergraph: Hypergraph, coloring: Coloring | None):
        """
        Вычисление разметки гиперграфа для этого способа:
            1) положения вершин
            2) положения ребер
            3) положение меток
        """
        ...

    @abstractmethod
    def _calculate_coloring(self, hypergraph: Hypergraph, coloring: Coloring | None):
        """
        Вычисление раскраски для этого гиперграфа:
        """
        ...

    @abstractmethod
    def _draw(self, axes: Axes, hypergraph: Hypergraph, coloring: Coloring | None):
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """
        :return: краткое описание этого способа отрисовки
        """
        ...
