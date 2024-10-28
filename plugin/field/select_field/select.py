from plugin.field import CdoField, BaseFieldEditWidget
from PySide6.QtWidgets import QComboBox, QLabel
from system import CdoApp
from plugin.field.select_field import SelectFieldValue

class SelectFieldLineEdit(QLabel):
    def __init__(self, field, saved_value):
        super().__init__()
        if saved_value != None:
            saved_value_data = SelectFieldValue.get(SelectFieldValue.id==int(saved_value))
            self.setText(saved_value_data.value)

class SelectFieldEditWidget(BaseFieldEditWidget):
    value = None

    def prepare_edit_widget(self):
        values_query = SelectFieldValue.select().where(SelectFieldValue.field==self.field)
        combo_box = QComboBox()
        values = []

        for i, v in enumerate(values_query.execute()):
            values.append(v)
            combo_box.addItem(v.value)
            if v.id == self.saved_value:
                combo_box.setCurrentIndex(i)

        combo_box.currentIndexChanged.connect(self.make_callback(self.on_item_selected, values))
        return combo_box
    
    def on_item_selected(self, values, index):
        self.value = values[index].id

    def get_value(self):
        return self.value

class SelectField(CdoField):
    name = "Select"
    edit_widget = SelectFieldEditWidget
    view_widget = SelectFieldLineEdit