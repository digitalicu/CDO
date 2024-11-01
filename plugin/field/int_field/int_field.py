from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QLineEdit

class IntFieldLineEdit(QLineEdit):
    def __init__(self, saved_value=None):
        super().__init__()
        if saved_value != None:
            self.setText(str(saved_value))

class IntFieldEditWidget(BaseFieldEditWidget):
    edit_widget_class = IntFieldLineEdit

    def get_value(self):
        return self.edit_widget.text()
    
    def set_value(self, value):
        self.edit_widget.setText(value)

class IntField(CdoField):
    name = "Integer"
    edit_widget = IntFieldEditWidget

    def clear_value(self, value):
        return int(value)