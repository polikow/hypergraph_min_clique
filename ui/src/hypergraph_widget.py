import ui

from ui.src.hypergraph_visualizers import *

from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class HypergraphWidget(FigureCanvasQTAgg):

    def __init__(self, parent):
        self.figure: Figure = Figure(
            dpi=ui.dpi(parent),
            tight_layout=True
        )
        self.figure.add_subplot(111)
        super(HypergraphWidget, self).__init__(self.figure)
        self.mpl_connect('button_press_event', self._clicked)

        # последний отрисованный гиперграф
        self.hypergraph: Hypergraph | None = None
        self.coloring: Coloring | None = None

        # все доступные способы визуализации гиперграфов
        self.visualizers = [
            visualizer()
            for visualizer in visualizers
        ]

        # текущий способ отображения гиперграфа
        self.visualizer = self.visualizers[0]

    @property
    def axes(self) -> Axes:
        return self.figure.axes[0]

    def clear(self):
        self.axes.clear()

    def draw_hypergraph(
            self,
            hypergraph: Hypergraph | None = None,
            coloring: Coloring | None = None,
            ignore_hash=False
    ):
        if hypergraph is None:
            if self.hypergraph is None:
                raise ValueError("Ни один граф еще ни разу не был отрисован")
            else:
                hypergraph = self.hypergraph

        if coloring == ():
            coloring = None
        elif coloring is None and hash(hypergraph) == hash(self.hypergraph):
            coloring = self.coloring

        visualizer_args = (self.axes, hypergraph, coloring)

        self.clear()
        if not ignore_hash:
            self.visualizer.draw(*visualizer_args)
        else:
            self.visualizer.draw_ignore_hash(*visualizer_args)
        self.draw()

        self.hypergraph = hypergraph
        self.coloring = coloring

    def _clicked(self, e: MouseEvent):
        if e.button == MouseButton.RIGHT:
            pos = self.mapToGlobal(e.guiEvent.pos())
            self.show_context_menu(pos)

    def show_context_menu(self, pos: QPoint):
        """
        Создание контекстного меню, в котором можно выбрать одну из 2х опций:
            1) перерисовать текущий граф
            2) переключится на следующий способ визуализации

        :param pos: место, в котором необходимо отобразить это контексное меню
        """
        menu = QMenu()

        redraw = menu.addAction("Перерисовать")
        change_visualizer = menu.addAction(
            f"Использовать {self.next_visualizer.description}"
        )

        action = menu.exec_(pos)

        if action == redraw:
            self.draw_hypergraph(ignore_hash=True)

        elif action == change_visualizer:
            self.use_next_visualizer()

        elif action is None:
            pass
        else:
            raise ValueError("Неизвестное действие")

    def use_next_visualizer(self):
        """
        Переключение на следующий способ визуализации
        """
        self.visualizer = self.next_visualizer

        # создание новой области отрисовки вместо старой
        # это необходимо для сохранения свойств tight_layout
        self.axes.remove()
        self.figure.add_subplot(111)

        self.draw_hypergraph()

    @property
    def next_visualizer(self) -> HypergraphVisualizer:
        """
        :return: следующий способ визуализации
        """
        curr_index = self.visualizers.index(self.visualizer)
        next_index = (curr_index + 1) % self.visualizers.__len__()
        return self.visualizers[next_index]
