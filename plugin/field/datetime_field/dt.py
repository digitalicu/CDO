from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QLineEdit, QGridLayout, QLabel, QDateTimeEdit
from PySide6.QtCore import QDateTime
from plugin.field_param import BaseFieldParam, BaseParamWidget
from peewee import *
from system import CdoApp
from model import CollectionField
import json
from datetime import datetime

class DateTimeSetting(Model):
    field = ForeignKeyField(CollectionField)
    key = CharField()
    value = CharField()

    class Meta:
        database = CdoApp.get_db()

class DateTimeLabel(QLabel):
    def __init__(self, field, saved_value):
        super().__init__()
        pattern_row = DateTimeSetting.get_or_none(DateTimeSetting.field==field, DateTimeSetting.key=="pattern")
        self.setText(saved_value.toString(pattern_row.value))
        
class DateTimeSettingsFieldParamWidget(BaseParamWidget):
    def __init__(self, field, field_processor, **kwargs):
        super(DateTimeSettingsFieldParamWidget, self).__init__(field, field_processor, **kwargs)
        self.build_layout()
    
    def build_layout(self):
        layout = QGridLayout()

        layout.addWidget(QLabel("Pattern"), 0, 0)
        self.pattern_edit = QLineEdit("dd.MM.yyyy")
        saved_pattern = self.get_setting_value("pattern")
        if saved_pattern is not None:
            self.pattern_edit.setText(saved_pattern)
        layout.addWidget(self.pattern_edit, 0, 1)

        self.setLayout(layout)

    def get_setting_value(self, key):
        if self.data.count() > 0:
            try:
                res = self.data.where(DateTimeSetting.key==key).get_or_none()
                if res is not None:
                    return res.value
            except Exception as e:
                pass
        return None

    def prepare_data(self):
        prepared_data = []
        if self.data.count() == 0:
            prepared_data.append(DateTimeSetting(
                field=self.field,
                key="pattern",
                value=self.pattern_edit.text()
            ))
        else:
            prepared_data = list(self.data.objects(DateTimeSetting))
            for o in prepared_data:
                if o.key == "pattern":
                    o.value = self.pattern_edit.text()
        return prepared_data
    
class DateTimeSettingsFieldParam(BaseFieldParam):
    include_field = ["plugin.field.datetime_field.DateTimeField"]

    title = "DateTime settings"
    model = DateTimeSetting
    param_widget = DateTimeSettingsFieldParamWidget

class DateTimeFieldLineEdit(QDateTimeEdit):
    def __init__(self, saved_value=None, pattern=None):
        super().__init__(QDateTime.currentDateTime())
        self.setDisplayFormat(pattern)
        if saved_value != None:
            self.setDateTime(saved_value)

class DateTimeFieldFieldEditWidget(BaseFieldEditWidget):
    edit_widget_class = DateTimeFieldLineEdit

    def get_value(self):
        return self.edit_widget.dateTime()
    
    def set_value(self, value):
        self.edit_widget.setText(value)

    def prepare_edit_widget(self):
        pattern_row = DateTimeSetting.get_or_none(DateTimeSetting.field==self.field, DateTimeSetting.key=="pattern")
        self.edit_widget = self.edit_widget_class(self.saved_value, pattern_row.value)
        return self.edit_widget

class DateTimeField(CdoField):
    name = "DateTime"
    edit_widget = DateTimeFieldFieldEditWidget
    view_widget = DateTimeLabel

    def pack(self, value):
        dt = value.toPython()
        return json.dumps({
            "value": dt.timestamp()
        })
    
    def unpack(self, value):
        data = json.loads(value)
        qt_time = QDateTime().fromSecsSinceEpoch(int(data["value"]))
        return qt_time