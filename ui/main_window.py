from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QScrollArea, QWidget
from PySide6.QtGui import Qt
from widget import BaseWidget, TextInputWindow, TextActionPanel, BaseMainWindow
from model import Collection, create_collection_by_name
from ui import CollectionEditWindow

class MainWindowCollections(BaseWidget):
    def __init__(self):
        super().__init__()
        self.build_layout()
        self.setLayout(self.layout)

    def build_layout(self):
        self.layout = QVBoxLayout()

        self.add_collection_btn = QPushButton("Add")
        self.add_collection_btn.clicked.connect(self.add_collection_btn_clicked)
        self.layout.addWidget(self.add_collection_btn)
        
        collections_data = Collection.select()
        if collections_data.count() > 0:
            frame = QWidget()
            frame_layout = QVBoxLayout()
            scrollable = QScrollArea()
            for c in collections_data:
                frame_layout.addWidget(TextActionPanel(c.name, [{
                    "title": "Edit",
                    "action": self.make_callback(self.on_collection_edit_clicked, [c]),
                }]))
            frame.setLayout(frame_layout)
            scrollable.setWidget(frame)
            self.layout.addWidget(scrollable)
    
    def on_collection_edit_clicked(self, collection: Collection):
        self.get_main_window(CdoMainWindow).set_collection_view(collection)
    
    def add_collection_btn_clicked(self):
        self.w = TextInputWindow(lambda value: self.create_collection_by_name(value))
        self.w.show()

    def create_collection_by_name(self, name):
        create_collection_by_name(name)
        self.get_main_window().update()

class CdoMainWindow(BaseMainWindow):
    central_widget = MainWindowCollections
    central_widget_kargs = []
    central_widget_kwargs = {}

    def __init__(self):
        super().__init__()
        # self.setWindowState(Qt.WindowMaximized)
        self.update_ui()

    def set_collection_view(self, collection: Collection):
        self.set_central_widget(CollectionEditWindow, [collection])
        
    def set_main_view(self):
        self.set_central_widget(MainWindowCollections)

    def closeEvent(self, event):
        event.accept()