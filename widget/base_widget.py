from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from system import CdoApp

class BaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db = CdoApp.get_db()

    def get_main_window(self, w_type=QMainWindow):
        for w in QApplication.topLevelWidgets():
            if type(w_type) == str:
                if w.__class__.__name__ == w_type:
                    return w
            elif isinstance(w, w_type):
                return w
            
    def make_callback(self, func, kargs=[], kwargs={}):
        def call():
            func(*kargs, **kwargs)
        return call
    
class BaseMainWindow(QMainWindow):
    central_widget = None
    central_widget_kargs = []
    central_widget_kwargs = {}

    def update_ui(self, **kwargs):
        self.central_widget_kwargs.update(kwargs)
        self.setCentralWidget(self.central_widget(*self.central_widget_kargs, **self.central_widget_kwargs))

    def set_central_widget(self, widget, kargs=[], kwargs={}):
        self.central_widget = widget
        self.central_widget_kargs = kargs
        self.central_widget_kwargs = kwargs
        self.update_ui()
        
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