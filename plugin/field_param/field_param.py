from system import CdoApp
from PySide6.QtWidgets import QWidget
from widget import BaseWidget
from multidict import MultiDict
from model import CollectionField
from plugin import BasePlugin

class BaseParamWidget(BaseWidget):
    collection = None
    data = None

    def __init__(self, field, field_processor):
        super(BaseParamWidget, self).__init__()
        self.field = field
        self.field_processor = field_processor
        self.load_model_data()

    def load_model_data(self):
        if self.field_processor.model == CollectionField:
            self.data = self.field
        else:
            self.data = self.field_processor.model.get(self.field_processor.model.field==self.field)

    def set_data(self, key, value):
        self.data.__dict__["__data__"][key] = value

    def prepare_data(self):
        return self.data

class BaseFieldParam(BasePlugin):
    exclude_field = []
    include_field = []

    title = ""

    model = None
    param_widget = None
    field_edit_param_widget = None
    field_view_param_widget = None

    def get_title(self) -> str:
        return self.title
    
    def get_param_widget(self, field: CollectionField):
        if self.param_widget is not None:
            return self.param_widget(field, self)
        return QWidget()
    
    def get_field_edit_param_widget(self):
        return self.field_edit_param_widget
    
    def get_field_view_param_widget(self):
        return self.field_view_param_widget
    
    def initialize(self):
        if self.model != None:
            CdoApp.get_db().create_tables([self.model])

    def field_applicable(self, field):
        if self.include_field != [] and field in self.include_field:
            return True
        elif self.include_field == [] and field not in self.exclude_field:
            return True
        return False