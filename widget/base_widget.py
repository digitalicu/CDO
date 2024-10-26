from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from system import CdoApp

class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = CdoApp.get_db()

    def get_main_window(self):
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QMainWindow):
                return w
            
    def make_callback(self, func, kargs=[], kwargs={}):
        def call():
            func(*kargs, **kwargs)
        return call
            
class BaseDataWidget(BaseWidget):
    data = {}

    def __init__(self, data={}):
        super().__init__()
        self.data = data

    def get_data(self, key=None):
        if key is None:
            return self.data
        else:
            return self.data[key]
    
    def set_data(self, key, value):
        self.data[key] = value

    def set_data_if(self, key, value, condition_value=None):
        if self.data[key] == condition_value:
            self.data[key] = value