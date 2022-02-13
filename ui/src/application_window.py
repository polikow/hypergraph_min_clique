import traceback

import ui
from hypergraph_utils import *
from PyQt5.QtWidgets import QApplication, QMainWindow


class ApplicationWindow(QMainWindow):

    def __init__(self, app_context: QApplication):
        super(ApplicationWindow, self).__init__()
        self.app_context = app_context
        self.ui = ui.MainWindow()
        self.ui.setupUi(self)

        self.ui.generateHypergraphButton.clicked.connect(self.generate_hypergraph)
        self.ui.findCliqueSeparatorButton.clicked.connect(self.find_min_clique_separator)

        self.hypergraph = generate_hypergraph(
            self.number_of_vertices,
            self.number_of_hyperedges
        )
        self.coloring = ()

        self.draw()

    @property
    def number_of_vertices(self) -> int:
        return self.ui.numberOfVerticesSpinBox.value()

    @property
    def number_of_hyperedges(self) -> int:
        return self.ui.numberOfHyperedgesSpinBox.value()

    def generate_hypergraph(self):
        self.hypergraph = generate_hypergraph(
            self.number_of_vertices,
            self.number_of_hyperedges
        )
        self.coloring = ()
        self.ui.resultTextEdit.setText("")
        self.draw()

    def find_min_clique_separator(self):
        try:
            cliques = find_minimal_clique_separators(self.hypergraph)
        except ValueError as e:
            self.ui.resultTextEdit.setText(f"{e}")
        except RuntimeError as e:
            self.ui.resultTextEdit.setText(f"{e}")
            traceback.print_exception(e)
        else:
            if len(cliques) == 0:
                self.ui.resultTextEdit.setText(f"У этого графа нет минимальных кликовых сепараторов")
            else:
                cliques = [set(c) for c in cliques]
                cliques.sort(key=lambda s: len(s))

                clique = f"Минимальный кликовый сепаратор:\n{cliques[0]}\n"
                other_cliques = ""
                if len(cliques) > 1:
                    other = "\n".join(str(c) for c in cliques[1:])
                    other_cliques = f"Остальные кликовые минимальные сепараторы:\n{other}"

                self.ui.resultTextEdit.setText(clique + other_cliques)
                self.coloring = [1 if node in clique else 0 for node in self.hypergraph.nodes]
                print(self.coloring)
                self.draw()

    def draw(self):
        self.ui.hypergraphWidget.draw_hypergraph(
            hypergraph=self.hypergraph,
            coloring=self.coloring
        )
