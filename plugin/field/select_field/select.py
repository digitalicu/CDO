from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QComboBox
from system import CdoApp
from plugin.field.select_field import SelectFieldValue

class SelectFieldEditWidget(BaseFieldEditWidget):
    def prepare_edit_widget(self):
        return QComboBox()

    def get_value(self):
        return None

class SelectField(CdoField):
    name = "Select"
    edit_widget = SelectFieldEditWidget

    # def clear_value(self, value):
    #     return int(value)