from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, QRect, Qt
from PySide6.QtGui import QPixmap, QPainterPath, QRegion

class ImagePixmapLabel(QLabel):
    clicked = Signal()

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self.item_width = 150
        self.radius = 5

        self.image = QPixmap(self.path).scaled(self.item_width, self.item_width, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        self.setFixedSize(self.item_width, self.item_width)
        self.setPixmap(self.image)

        rounded_rect = QPainterPath()
        rounded_rect.addRoundedRect(QRect(0, 0, self.item_width, self.item_width), self.radius, self.radius)
        region = QRegion(rounded_rect.toFillPolygon().toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)