from system import Initializer, CdoApp
from PySide6.QtWidgets import QApplication
import sys

from ui import CdoMainWindow

app_init = Initializer()
app_init.preapre_app()

app = QApplication(sys.argv)
main_window = CdoMainWindow()
main_window.show()
app.exec()