from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QTableWidgetItem, QLabel
from widget import BaseWidget
from system import CdoApp
from model import CollectionField
from plugin import BasePlugin
import json

class CdoFieldLineEdit(QLineEdit):
    def __init__(self, saved_value=None):
        super().__init__()
        if saved_value != None:
            self.setText(saved_value)

class BaseFieldWidget(BaseWidget):
    def __init__(self, field: CollectionField):
        super().__init__()
        self.field = field
        layout = self.build_layout()
        self.setLayout(layout)

    def build_layout(self):
        return QVBoxLayout()

class BaseFieldViewWidget(BaseFieldWidget):
    def __init__(self, field: CollectionField, value):
        self.value = value
        super(BaseFieldViewWidget, self).__init__(field)

    def build_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(str(self.value)))
        self.setMinimumHeight(35)
        return layout

class BaseFieldEditWidget(BaseFieldWidget):
    edit_widget_class = None
    edit_widget = None

    def __init__(self, field: CollectionField, saved_value=None):
        self.saved_value = saved_value
        self.field_param_plugins = CdoApp.get_applicable_plugins(field.type.package)
        super(BaseFieldEditWidget, self).__init__(field)

    def build_layout(self):
        layout = QVBoxLayout()
        field_param_widgets = self.prepare_field_param_widgets()
        layout.addWidget(self.prepare_widget(field_param_widgets))
        return layout
    
    def prepare_field_param_widgets(self):
        # print(self.field_param_plugins)
        return []
    
    def prepare_widget(self, field_param_widgets=[]):
        prepared_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.prepare_edit_widget())
        prepared_widget.setLayout(layout)
        return prepared_widget
    
    def prepare_edit_widget(self):
        self.edit_widget = self.edit_widget_class(self.saved_value)
        return self.edit_widget
    
    def get_value(self):
        return None
    
    def set_value(self, value):
        pass

class CdoField(BasePlugin):
    name = ""
    view_widget = BaseFieldViewWidget
    edit_widget = BaseFieldEditWidget

    def get_name(self) -> str:
        return self.name
    
    def get_view_widget(self, field: CollectionField, value) -> QWidget:
        return self.view_widget(field, value)
    
    def get_edit_widget(self, field: CollectionField, saved_value=None) -> QWidget:
        return self.edit_widget(field, saved_value)
    
    def clear_value(self, value):
        return value
    
    def pack(self, value):
        return json.dumps({
            "value": value
        })
    
    def unpack(self, value):
        data = json.loads(value)
        return data["value"]