from peewee import *
from system import CdoApp
from model import CollectionField
from plugin.field_param import BaseFieldParam, BaseParamWidget
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit

class SelectFieldValue(Model):
    field = ForeignKeyField(CollectionField)
    value = CharField()

    class Meta:
        database = CdoApp.get_db()

class SelectOptionsParamWidget(BaseParamWidget):
    def __init__(self, field, field_processor):
        super(SelectOptionsParamWidget, self).__init__(field, field_processor)
        layout = QGridLayout()

        # layout.addWidget(QLabel("Name"), 0, 0)
        # self.name_edit = QLineEdit(self.data.name)
        # self.name_edit.textChanged.connect(lambda t: self.set_data("name", t))
        # layout.addWidget(self.name_edit, 0, 1)

        self.setLayout(layout)

    def load_model_data(self):
        self.data = SelectFieldValue.select().where(self.field_processor.model.field==self.field).execute()
        print(self.data)

class SelectOptionsFieldParam(BaseFieldParam):
    include_field = ["plugin.field.select_field.SelectField"]

    title = "Options"
    model = SelectFieldValue
    param_widget = SelectOptionsParamWidget