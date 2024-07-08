from PySide6.QtWidgets import QHBoxLayout, QSpacerItem, QLabel, QSizePolicy
from PySide6.QtGui import QMovie

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
        self.label.setMovie(self.movie)
    
    def start(self):
        self.setEnabled(True)
        self.movie.start()
    
    def stop(self):
        self.setEnabled(False)
        self.movie.deleteLater()
