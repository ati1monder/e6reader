from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, QRect, Qt
from PySide6.QtGui import QPixmap, QPainterPath, QRegion, QPainter, QColor

class ImagePixmapLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.item_width = 150
        self.radius = 5

        self.setFixedSize(self.item_width, self.item_width)

        rounded_rect = QPainterPath()
        rounded_rect.addRoundedRect(QRect(0, 0, self.item_width, self.item_width), self.radius, self.radius)
        region = QRegion(rounded_rect.toFillPolygon().toPolygon())
        self.setMask(region)

    def addImage(self, path):
        self.image = QPixmap(path).scaled(self.item_width, self.item_width, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        self.setPixmap(self.image)

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QColor('#C7C7C7'))
        painter.setPen(Qt.PenStyle.NoPen)
        rounded_rect = QPainterPath()
        rounded_rect.addRoundedRect(QRect(0, 0, self.item_width, self.item_width), self.radius, self.radius)
        painter.drawPath(rounded_rect)

        super().paintEvent(event)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)