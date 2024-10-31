from plugin.field_param import BaseFieldParam, BaseParamWidget, BaseFieldParamEditWidget
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton
from peewee import *
from model import CollectionField
from system import CdoApp
from widget import ErrorWindow, TextActionPanel

class PresetFieldValue(Model):
    field = ForeignKeyField(CollectionField)
    value = CharField()
    order = IntegerField(default=0)

    class Meta:
        database = CdoApp.get_db()

class PresetOptionWidget(BaseParamWidget):
    def __init__(self, field, field_param_processor, **kwargs):
        super(PresetOptionWidget, self).__init__(field, field_param_processor, **kwargs)
        layout = QGridLayout()
        
        self.fp = CdoApp.get_plugins()["FIELD_PLUGIN"][field.type.package]
        self.edit_widget = self.fp.get_edit_widget(field)
        layout.addWidget(self.edit_widget, 0, 0)

        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.on_add_btn_clicked)
        layout.addWidget(add_btn, 0, 1)

        row = 1
        for preset in self.data.execute():
            layout.addWidget(TextActionPanel(preset.value), row, 0, 1, 2)
            row+=1

        self.setLayout(layout)

    def on_add_btn_clicked(self):
        value = self.edit_widget.get_value()

        try:
            clear_field_value = self.fp.clear_value(value)
            self.add_new_preset(clear_field_value)
            self.get_main_window("FieldEditWindow").update_ui(tab_index=self.tab_index)
        except Exception as e:
            self.w = ErrorWindow(errors=[
                {
                    "text": "%s" % (str(e))
                }
            ])
            self.w.show()

    def add_new_preset(self, value):
        PresetFieldValue.create(field=self.field, value=value)

    def prepare_data(self):
        return None
    
class PresetOptionFieldParamEditWidget(BaseFieldParamEditWidget):
    def __init__(self, field, field_processor, base_param_widget):
        super(PresetOptionFieldParamEditWidget, self).__init__(field, field_processor, base_param_widget)
        if self.data.count() == 0:
            self.is_empty = True
        else:
            layout = QGridLayout()
            
            for preset_data in self.data:
                preset_btn = QPushButton(preset_data.value)
                preset_btn.clicked.connect(self.make_callback(self.on_preset_btn_clicked, preset_data.value))
                layout.addWidget(preset_btn)

            self.setLayout(layout)

    def on_preset_btn_clicked(self, value):
        self.base_param_widget.set_value(value)

class PresetOptionFieldParam(BaseFieldParam):
    include_field = [
        "plugin.field.int_field.IntField",
        "plugin.field.string_field.StringField",
    ]

    title = "Presets"
    model = PresetFieldValue
    param_widget = PresetOptionWidget
    field_edit_param_widget = PresetOptionFieldParamEditWidget