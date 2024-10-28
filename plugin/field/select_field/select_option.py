from peewee import *
from system import CdoApp
from model import CollectionField
from ui import FieldEditWindow
from widget import TextActionPanel
from plugin.field_param import BaseFieldParam, BaseParamWidget
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton

class SelectFieldValue(Model):
    field = ForeignKeyField(CollectionField)
    value = CharField()

    class Meta:
        database = CdoApp.get_db()

class SelectOptionsParamWidget(BaseParamWidget):
    def __init__(self, field, field_processor, **kwargs):
        super(SelectOptionsParamWidget, self).__init__(field, field_processor, **kwargs)
        self.build_layout()
    
    def build_layout(self):
        layout = QGridLayout()

        self.new_option_edit = QLineEdit()
        layout.addWidget(self.new_option_edit, 0, 0)

        self.new_option_add_btn = QPushButton("Add")
        self.new_option_add_btn.clicked.connect(self.on_new_option_add_btn)
        layout.addWidget(self.new_option_add_btn, 0, 1)

        row = 1
        for d in self.data:
            layout.addWidget(TextActionPanel(d.value), row, 0)
            row += 1

        self.setLayout(layout)

    def on_new_option_add_btn(self):
        value = self.new_option_edit.text()
        if len(value) > 0:
            SelectFieldValue.create(field=self.field, value=self.new_option_edit.text())
            self.new_option_edit.setText("")
            self.load_model_data()
            self.get_main_window(FieldEditWindow).update_ui(tab_index=self.tab_index)

    def load_model_data(self):
        self.data = SelectFieldValue.select().where(self.field_processor.model.field==self.field).execute()

    def prepare_data(self):
        return None

class SelectOptionsFieldParam(BaseFieldParam):
    include_field = ["plugin.field.select_field.SelectField"]

    title = "Options"
    model = SelectFieldValue
    param_widget = SelectOptionsParamWidget