from PySide6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout, QTabWidget, QComboBox
from widget import BaseMainWindow, BaseWidget
from system import CdoApp
from model import CollectionField

class FieldEditCentralWidget(BaseWidget):
    def __init__(self, field: CollectionField = None, tab_index=0):
        super().__init__()
        self.tab_index=tab_index
        self.field = field
        self.field_plugin_processor = CdoApp.get_plugins()["FIELD_PLUGIN"][field.type.package]

        self.field_param_plugins = {}
        self.param_tab_widgets = {}

        self.build_layout()

    def build_layout(self):
        layout = QVBoxLayout()

        self.tab_bar = QTabWidget()
        for package, param_plugin in CdoApp.get_plugins()["FIELD_PARAM_PLUGIN"].items():
            self.field_param_plugins[package] = param_plugin
            if param_plugin.field_applicable(self.field.type.package):
                param_tab_widget = param_plugin.get_param_widget(self.field, tab_index=self.tab_bar.count())
                self.tab_bar.addTab(param_tab_widget, param_plugin.get_title())
                self.param_tab_widgets[package] = param_tab_widget
        self.tab_bar.setCurrentIndex(self.tab_index)
        layout.addWidget(self.tab_bar)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save_btn_click)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def update_ui(self, tab_index=0):
        self.build_layout()

    def on_save_btn_click(self):
        for package, ptw in self.param_tab_widgets.items():
            data = ptw.prepare_data()
            if data is not None:
                data.save()
        self.get_main_window("CdoMainWindow").update_ui(tab_index=1)
        self.close()

class FieldEditWindow(BaseMainWindow):
    central_widget = FieldEditCentralWidget

    def __init__(self, field: CollectionField = None):
        super().__init__()
        self.central_widget_kargs = [field]
        self.update_ui()