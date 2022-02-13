from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QWidget


def dpi(elem: QApplication | QWidget | QObject) -> int:
    """
    :param elem: объект PyQT, для которого нужно найти оптимальный dpi
    :return: оптимальный dpi
    """
    if isinstance(elem, QApplication):
        return app_dpi(elem)

    elif isinstance(elem, (QWidget, QObject)):
        if hasattr(elem, "app_context"):
            app = elem.app_context
            return app_dpi(app)
        else:
            try:
                parent_elem = elem.parent()
                return dpi(parent_elem)
            except ValueError:
                raise ValueError(
                    f"У элемента \"{elem}\" и всех его родителей нет аттрибута \"app_context\""
                )
    else:
        raise ValueError(f"Для элемента \"{elem}\" нельзя найти dpi")


def app_dpi(app: QApplication) -> int:
    """
    :param app: приложение, для которого нужно найти оптимальный dpi
    :return: оптимальный dpi
    """
    screen = app.screens()[0]
    dpi_float = screen.physicalDotsPerInch()
    dpi_int = int(dpi_float)
    return dpi_int
