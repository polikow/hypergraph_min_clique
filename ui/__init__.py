import os

# автоматически конвертирует из .ui в .py при запуске main
import platform

if platform.system() == "Linux":
    os.system("./ui/convert.sh")

from ui.converted.main_window import Ui_MainWindow as MainWindow
from ui.src.application_window import ApplicationWindow
from ui.utils import dpi
