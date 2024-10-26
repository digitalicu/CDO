from PySide6.QtWidgets import QVBoxLayout, QPushButton, QTabWidget, QComboBox, QGridLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem
from widget import BaseWidget, ScrollableActionPanelList
from model import Collection, CollectionField, Plugin
from system import CdoApp
from ui import FieldEditWindow, CollectionDataEditWindow

class BaseCollectionTab(BaseWidget):
    def __init__(self, collection: Collection, tab_index: int = 0):
        super().__init__()
        self.setMinimumWidth(500)
        self.collection = collection
        self.tab_index = tab_index

    def on_selected(self):
        pass

class CollectionFieldsView(BaseCollectionTab):
    def __init__(self, collection: Collection, tab_index: int = 0):
        super(CollectionFieldsView, self).__init__(collection, tab_index)
        self.field_plugins = CdoApp.get_plugins()["FIELD_PLUGIN"]
        self.build_layout()

    def build_layout(self):
        layout = QGridLayout()

        row = 0

        self.new_field_name = QLineEdit()
        layout.addWidget(self.new_field_name, row, 0)

        self.new_field_type_select = QComboBox()
        self.new_field_type_select.addItems([t.get_name() for t in self.field_plugins.values()])
        layout.addWidget(self.new_field_type_select, row, 1)

        self.new_field_btn = QPushButton("Add")
        self.new_field_btn.clicked.connect(self.on_new_field_btn_clicked)
        layout.addWidget(self.new_field_btn, row, 2)

        row += 1

        if self.collection.fields.count() > 0:
            field_list = []
            for f in self.collection.fields:
                field_list.append((f.name, [{
                    "title": "Edit",
                    "action": self.make_callback(self.on_field_edit_clicked, [f])
                }]))
            field_list_view = ScrollableActionPanelList(field_list)
            layout.addWidget(field_list_view, row, 0, 1, 3)
            row += 1

        self.setLayout(layout)

    def on_new_field_btn_clicked(self):
        field_plugin_package = list(self.field_plugins.keys())[self.new_field_type_select.currentIndex()]
        new_field_name = self.new_field_name.text()
        new_field_plugin = Plugin.get(Plugin.package==field_plugin_package)
        new_field = CollectionField.create(name=new_field_name, collection=self.collection, type=new_field_plugin)
        self.get_main_window().update(tab_index=self.tab_index)

    def on_field_edit_clicked(self, field: CollectionField):
        self.w = FieldEditWindow(field)
        self.w.show()

class CollectionDetailsView(BaseCollectionTab):
    def __init__(self, collection: Collection, tab_index: int = 0):
        super(CollectionDetailsView, self).__init__(collection, tab_index)
        layout = QGridLayout()

        layout.addWidget(QLabel("Name"), 0, 0)
        self.collection_name_edit = QLineEdit(collection.name)
        layout.addWidget(self.collection_name_edit, 0 , 1)

        self.save_collection_details_btn = QPushButton("Save")
        self.save_collection_details_btn.clicked.connect(self.on_save_colection_btn_clicked)
        layout.addWidget(self.save_collection_details_btn, 1, 0, 1, 2)

        self.setLayout(layout)

    def on_save_colection_btn_clicked(self):
        self.collection.name = self.collection_name_edit.text()
        self.collection.save()
        self.get_main_window().set_main_view()

class СollectionDataView(BaseCollectionTab):
    def __init__(self, collection: Collection, tab_index: int = 0):
        super(СollectionDataView, self).__init__(collection, tab_index)
        self.build_layout()

    def build_layout(self):
        layout = QVBoxLayout()

        self.add_data_entity_btn = QPushButton("add")
        self.add_data_entity_btn.clicked.connect(self.on_add_data_entity_btn_clicked)
        layout.addWidget(self.add_data_entity_btn)

        self.data_table = QTableWidget()
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.data_table.cellDoubleClicked.connect(self.on_data_table_cell_double_clicked)
        self.prepare_data_rows()
        layout.addWidget(self.data_table)

        self.setLayout(layout)

    def prepare_data_rows(self):
        rows = self.collection.rows

        self.data_table.setColumnCount(self.collection.fields.count())
        self.data_table.setHorizontalHeaderLabels([f.name for f in self.collection.fields])
        self.data_table.verticalHeader().hide()
        self.data_table.setRowCount(rows.count())

        for ri, r in enumerate(rows):
            for ci, fd in enumerate(r.fields):
                plugin_processor = CdoApp.get_plugins()["FIELD_PLUGIN"][fd.field.type.package]
                value = plugin_processor.unpack(fd.value)
                self.data_table.setContentsMargins(0,0,0,0)
                self.data_table.setCellWidget(ri, ci, plugin_processor.get_view_widget(fd.field, value))

    def on_data_table_cell_double_clicked(self, ri, ci):
        self.w = CollectionDataEditWindow(self.collection, ri)
        self.w.show()

    def on_add_data_entity_btn_clicked(self):
        self.w = CollectionDataEditWindow(self.collection)
        self.w.show()

class CollectionEditWindow(BaseWidget):
    tab_widgets = []

    def __init__(self, collection: Collection, tab_index: int = 0):
        super().__init__()
        self.collection = collection

        layout = QVBoxLayout()

        self.tab_widgets = [
            (CollectionDetailsView(collection, 0), "General"),
            (CollectionFieldsView(collection, 1), "Fields"),
            (СollectionDataView(collection, 2), "Data")
        ]

        self.tab_bar = QTabWidget()
        for tw in self.tab_widgets:
            self.tab_bar.addTab(*tw)
        self.tab_bar.currentChanged.connect(self.on_tab_changed)
        self.tab_bar.setCurrentIndex(tab_index)
        layout.addWidget(self.tab_bar)

        self.setLayout(layout)

    def on_tab_changed(self, index):
        self.tab_widgets[index][0].on_selected()