from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class InfoImageBox(QWidget):
    def __init__(self, object, info, parent = None):
        super().__init__(parent)
        self.info = info

        self.setContentsMargins(0, 0, 0, 0)

        self.vert_box = QVBoxLayout()
        self.setLayout(self.vert_box)
        self.vert_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vert_box.setContentsMargins(0,0,0,0)

        self.horiz_box = QHBoxLayout()
        self.horiz_box.setContentsMargins(0,0,0,0)

        self.object = object
        self.vert_box.addWidget(self.object)
        self.vert_box.addLayout(self.horiz_box)

        label = QLabel()
        label.setText(f'id: {info["id"]}')
        label.setStyleSheet("QLabel{ color: #C7C7C7; }")
        self.horiz_box.addWidget(label)

    def on_loaded():
        pass
