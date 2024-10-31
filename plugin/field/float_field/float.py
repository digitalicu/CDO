from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QLineEdit

class FloatFieldLineEdit(QLineEdit):
    def __init__(self, saved_value=None):
        super().__init__()
        if saved_value != None:
            self.setText(str(saved_value))

class FloatFieldEditWidget(BaseFieldEditWidget):
    edit_widget_class = FloatFieldLineEdit

    def get_value(self):
        return float(self.edit_widget.text())
    
    def set_value(self, value):
        self.edit_widget.setText(value)

class FloatField(CdoField):
    name = "Float"
    edit_widget = FloatFieldEditWidget

    def clear_value(self, value):
        return float(value)