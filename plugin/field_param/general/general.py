from plugin.field_param import BaseFieldParam, BaseParamWidget
from model import CollectionField
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit

class GeneralParamWidget(BaseParamWidget):
    def __init__(self, field, field_processor):
        super(GeneralParamWidget, self).__init__(field, field_processor)
        layout = QGridLayout()

        layout.addWidget(QLabel("Name"), 0, 0)
        self.name_edit = QLineEdit(self.data.name)
        self.name_edit.textChanged.connect(lambda t: self.set_data("name", t))
        layout.addWidget(self.name_edit, 0, 1)

        self.setLayout(layout)

class GeneralFieldParam(BaseFieldParam):
    title = "General"
    model = CollectionField
    param_widget = GeneralParamWidget