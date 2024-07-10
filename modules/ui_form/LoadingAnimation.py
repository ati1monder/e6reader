from PySide6.QtWidgets import QHBoxLayout, QSpacerItem, QLabel, QSizePolicy
from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize

class LoadingAnimation(QHBoxLayout):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.left_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.right_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.label = QLabel()


        self.addItem(self.left_spacer)
        self.addWidget(self.label)
        self.addItem(self.right_spacer)

        self.movie = QMovie('./assets/loading.gif')
        self.movie.setScaledSize(QSize(64, 64))
        self.label.setMovie(self.movie)
    
    def start(self):
        self.label.setVisible(True)
        self.movie.start()
    
    def stop(self):
        self.movie.stop()
        self.label.setVisible(False)
