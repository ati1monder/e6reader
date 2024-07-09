from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt

class InfoImageBox(QWidget):
    def __init__(self, object, parent = None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)

        self.vert_box = QVBoxLayout()
        self.setLayout(self.vert_box)
        self.vert_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.vert_box.setContentsMargins(0,0,0,0)

        self.horiz_box = QHBoxLayout()
        self.horiz_box.setContentsMargins(0,0,0,0)
        self.horiz_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.object = object
        self.vert_box.addWidget(self.object)
        self.vert_box.addLayout(self.horiz_box)

        label = QLabel()
        label.setText('----Unknown----')
        label.setStyleSheet("QLabel{ color: #C7C7C7; }")
        self.horiz_box.addWidget(label)

    def on_loaded():
        pass
