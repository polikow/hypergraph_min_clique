import sys
import ui
from PyQt5.QtWidgets import QApplication, QStyleFactory

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle(QStyleFactory.create('Fusion'))

    window = ui.ApplicationWindow(app_context=app)
    window.show()

    sys.exit(app.exec())
