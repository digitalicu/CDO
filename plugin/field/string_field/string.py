from plugin.field import CdoField, BaseFieldEditWidget, CdoFieldLineEdit

class StringFieldEditWidget(BaseFieldEditWidget):
    edit_widget_class = CdoFieldLineEdit

    def get_value(self):
        return self.edit_widget.text()

class StringField(CdoField):
    name = "String"
    edit_widget = StringFieldEditWidget