from PySide6.QtWidgets import QVBoxLayout, QPushButton, QGridLayout, QTabWidget, QComboBox, QWidget, QHBoxLayout, QGroupBox
from widget import BaseWidget, BoxWidget, ErrorWindow, ScrollableList
from system import CdoApp
from model import Collection, CollectionDataRow, CollectionFieldValue, CollectionField

class CollectionFieldDataEditWidget(BaseWidget):
    plugin_widgets = {}

    def __init__(self, field: CollectionField, row):
        super().__init__()
        self.field = field
        self.row = row
        self.field_processor = CdoApp.get_plugins()["FIELD_PLUGIN"][self.field.type.package]
        self.build_layout()

    def build_layout(self):
        layout = QHBoxLayout()

        self.base_param_widget = self.prepare_base_param_widget()
        layout.addWidget(self.base_param_widget)

        applicable_plugins = CdoApp.get_applicable_plugins(self.field.type.package)
        for ppackage, plugin_processor in applicable_plugins.items():
            plugin_widget_class = plugin_processor.get_field_edit_param_widget()
            if plugin_widget_class is not None:
                plugin_widget = plugin_widget_class(self.field, plugin_processor, self.base_param_widget)
                if not plugin_widget.is_empty:
                    layout.addWidget(plugin_widget)

                self.plugin_widgets[ppackage] = plugin_widget

        self.box(layout)

    def box(self, panel_widget_layout):
        layout = QVBoxLayout()
        box = QGroupBox(self.field.name)
        box.setLayout(panel_widget_layout)
        layout.addWidget(box)
        self.setLayout(layout)

    def prepare_base_param_widget(self):
        saved_field_value = None
        if self.row is not None:
            saved_field_data = self.row.fields.where(CollectionFieldValue.field==self.field).get_or_none()
            if saved_field_data is not None:
                saved_field_value = self.field_processor.unpack(saved_field_data.value)

        field_prepared_widget = self.field_processor.get_edit_widget(self.field, saved_field_value)

        return field_prepared_widget
    
    def get_value(self):
        base_value = self.base_param_widget.get_value()
        for ppackage, pwidget in self.plugin_widgets.items():
            base_value = pwidget.process_value(base_value)

        return base_value

class CollectionDataEditWindow(BaseWidget):
    field_utilities = {}
    prepared_values = {}
    row = None

    def __init__(self, collection: Collection = None, row_index = None):
        super().__init__()
        self.collection = collection

        if row_index != None:
            self.load_row_data(row_index)

        self.build_layout()

    def load_row_data(self, row_index):
        self.row = list(self.collection.rows)[row_index]

    def build_layout(self):
        layout = QGridLayout()

        field_widgets = []
        for f in self.collection.fields:
            field_processor = CdoApp.get_plugins()["FIELD_PLUGIN"][f.type.package]
            field_prepared_widget = CollectionFieldDataEditWidget(f, self.row)
            field_widgets.append(field_prepared_widget)
            self.field_utilities[f.id] = {
                "processor": field_processor,
                "widget": field_prepared_widget
            }

        layout.addWidget(ScrollableList(widgets=field_widgets))

        self.add_data_row_btn = QPushButton("Save")
        self.add_data_row_btn.clicked.connect(self.on_save_data_row_btn_clicked)
        layout.addWidget(self.add_data_row_btn)

        self.setLayout(layout)

    def on_save_data_row_btn_clicked(self):
        errors = []
        for f in self.collection.fields:
            field_value = self.field_utilities[f.id]["widget"].get_value()
            try:
                clear_field_value = self.field_utilities[f.id]["processor"].clear_value(field_value)
                self.prepared_values[f.id] = clear_field_value
            except Exception as e:
                errors.append({
                    "text": "%s: %s" % (f.name, str(e))
                })

        if len(errors) > 0:
            self.e = ErrorWindow(errors)
            self.e.show()
        else:
            self.save_row()

    def save_row(self):
        if len(self.prepared_values.keys()) > 0:
            if self.row is None:
                self.create_new_row()
            else:
                self.save_existed_row()

        self.get_main_window("CdoMainWindow").update_ui(tab_index=2)        
        self.close()

    def save_existed_row(self):
        for fid, value in self.prepared_values.items():
            try:
                db_field_value = CollectionFieldValue.get(CollectionFieldValue.field==CollectionField.get(CollectionField.id==fid),
                                                          CollectionFieldValue.row==self.row)
                db_field_value.value = self.field_utilities[fid]["processor"].pack(value)
                db_field_value.save()
            except Exception as e:
                CollectionFieldValue.create(field=CollectionField.get(CollectionField.id==fid), 
                                            row=self.row, 
                                            value=self.field_utilities[fid]["processor"].pack(value))

    def create_new_row(self):
        data_row = CollectionDataRow.create(collection=self.collection)
        for fid, value in self.prepared_values.items():
            CollectionFieldValue.create(field=CollectionField.get(CollectionField.id==fid), 
                                        row=data_row, 
                                        value=self.field_utilities[fid]["processor"].pack(value))