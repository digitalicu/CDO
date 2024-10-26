from PySide6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout, QTabWidget, QComboBox
from widget import BaseWidget
from system import CdoApp
from model import CollectionField

class FieldEditWindow(BaseWidget):
    def __init__(self, field: CollectionField = None):
        super().__init__()
        self.field = field
        self.field_plugin_processor = CdoApp.get_plugins()["FIELD_PLUGIN"][field.type.package]

        self.field_param_plugins = {}
        self.param_tab_widgets = {}

        layout = QVBoxLayout()

        self.tab_bar = QTabWidget()
        for package, param_plugin in CdoApp.get_plugins()["FIELD_PARAM_PLUGIN"].items():
            self.field_param_plugins[package] = param_plugin
            if param_plugin.field_applicable(self.field.type.package):
                param_tab_widget = param_plugin.get_param_widget(self.field)
                self.tab_bar.addTab(param_tab_widget, param_plugin.get_title())
                self.param_tab_widgets[package] = param_tab_widget
        layout.addWidget(self.tab_bar)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save_btn_click)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def on_save_btn_click(self):
        for package, ptw in self.param_tab_widgets.items():
            data = ptw.prepare_data()
            data.save()
        self.get_main_window().update(tab_index=1)
        self.close()