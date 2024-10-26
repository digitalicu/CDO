from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QCheckBox

class BoolFieldWidget(QCheckBox):
    def __init__(self, saved_value=None):
        super().__init__()
        if saved_value != None:
            self.setChecked(saved_value)

class BoolFieldEditWidget(BaseFieldEditWidget):
    edit_widget_class = BoolFieldWidget

    def get_value(self):
        return self.edit_widget.isChecked()

class BooleanField(CdoField):
    name = "Boolean"
    edit_widget = BoolFieldEditWidget

    def clear_value(self, value):
        return bool(value)