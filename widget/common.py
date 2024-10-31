from PySide6.QtWidgets import QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QGroupBox, QLabel
from widget import BaseWidget

class ErrorWindow(BaseWidget):
    def __init__(self, errors=[]):
        super().__init__()
        layout = QVBoxLayout()

        for e in errors:
            layout.addWidget(QLabel(e["text"]))

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.clicked.connect(self.on_ok_btn_clicked)
        layout.addWidget(self.ok_btn)

        self.setLayout(layout)

    def on_ok_btn_clicked(self):
        self.close()

class BoxWidget(BaseWidget):
    def __init__(self, title, widget):
        super().__init__()

        box = QGroupBox(title)
        global_layout = QVBoxLayout()
        layout = QVBoxLayout()
        layout.addWidget(widget)
        box.setLayout(layout)
        global_layout.addWidget(box)
        self.setLayout(global_layout)

class ScrollableList(BaseWidget):
    widgets = []

    def __init__(self, widgets=[]):
        super().__init__()
        self.widgets = widgets

        frame = QWidget()
        frame_layout = QVBoxLayout()
        scrollable = QScrollArea()

        for w in widgets:
            frame_layout.addWidget(w)
            
        frame.setLayout(frame_layout)
        scrollable.setWidget(frame)

        self_layout = QVBoxLayout()
        self_layout.addWidget(scrollable)
        self.setLayout(self_layout)

class ScrollableActionPanelList(BaseWidget):
    panels = []
    def __init__(self, panels=[]):
        super().__init__()
        panel_widgets = self.build_panel_list(panels)

        frame = QWidget()
        frame_layout = QVBoxLayout()
        scrollable = QScrollArea()

        for pw in panel_widgets:
            frame_layout.addWidget(pw)
            
        frame.setLayout(frame_layout)
        scrollable.setWidget(frame)

        self_layout = QVBoxLayout()
        self_layout.addWidget(scrollable)
        self.setLayout(self_layout)

    def build_panel_list(self, panels):
        panel_widgets = []
        for p in panels:
            panel_widgets.append(TextActionPanel(*p))

        return panel_widgets

class TextActionPanel(BaseWidget):
    def __init__(self, text, actions=[]):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        text_label = QLabel(text)
        layout.addWidget(text_label)

        for a in actions:
            b = QPushButton(a["title"])
            b.clicked.connect(a["action"])
            layout.addWidget(b)

        self.setLayout(layout)

class TextInputWindow(BaseWidget):
    def __init__(self, callback=None, button_text="Add"):
        super().__init__()
        self.callback_sent = False
        self.callback = callback

        layout = QVBoxLayout()

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.event_btn = QPushButton(button_text)
        self.event_btn.clicked.connect(self.event_btn_clicked)
        layout.addWidget(self.event_btn)

        self.setLayout(layout)

    def event_btn_clicked(self):
        self.callback(self.input_field.text())
        self.callback_sent = True
        self.close()

    def closeEvent(self, event):
        if not self.callback_sent:
            self.callback(None)
        event.accept()