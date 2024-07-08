from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, QRect, Qt
from PySide6.QtGui import QPixmap, QPainterPath, QRegion

class ImagePixmapLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_width = 150

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def appendImage(self, path):
        image = QPixmap(path).scaled(self.item_width, self.item_width, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        self.setFixedSize(self.item_width, self.item_width)
        self.setPixmap(image)

        rounded_rect = QPainterPath()
        radius = 5
        rounded_rect.addRoundedRect(QRect(0, 0, self.item_width, self.item_width), radius, radius)
        region = QRegion(rounded_rect.toFillPolygon().toPolygon())
        self.setMask(region)