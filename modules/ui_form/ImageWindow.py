from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize

class ImageWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.path = None
        self.setMinimumSize(640, 450)

        self.verticalMainLayout = QVBoxLayout(self)

        self.listButtonLayout = QHBoxLayout()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.controlButtonLayout = QHBoxLayout()

        # adding mainLayout and listButtonLayout to verticalMainLayout
        self.verticalMainLayout.addLayout(self.listButtonLayout)
        self.verticalMainLayout.addLayout(self.mainLayout)

        # verticalMainLayout->listButtonLayout
        self.nextButton = QPushButton(text="Next")
        self.prevButton = QPushButton(text="Previous")
        self.horizSpacer1 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Ignored)
        self.horizSpacer2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)

        # verticalMainLayout->mainLayout->imageLabelCentered
        self.imageLabelLayout = QHBoxLayout()
        self.imageLabelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageHorizSpacerLeft = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.imageHorizSpacerRight = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.imageLabel = QLabel()
        self.imageLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        # verticalMainLayout->mainLayout->controlButtonLayout
        self.upButton = QPushButton(text="Up")
        self.downButton = QPushButton(text="Down")
        self.favButton = QPushButton(text="Favourite")
        self.horizSpacer3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.downloadButton = QPushButton(text="Download")

        # add items to verticalMainLayout->mainLayout->imageLabelCentered
        self.imageLabelLayout.addSpacerItem(self.imageHorizSpacerLeft)
        self.imageLabelLayout.addWidget(self.imageLabel)
        self.imageLabelLayout.addSpacerItem(self.imageHorizSpacerRight)

        # add items to verticalMainLayout->mainLayout
        self.mainLayout.addLayout(self.imageLabelLayout)
        self.mainLayout.addSpacerItem(self.verticalSpacer)
        self.mainLayout.addLayout(self.controlButtonLayout)
        
        # add items to verticalMainLayout->mainLayout->controlButtonLayout
        self.controlButtonLayout.addWidget(self.upButton)
        self.controlButtonLayout.addWidget(self.downButton)
        self.controlButtonLayout.addWidget(self.favButton)
        self.controlButtonLayout.addSpacerItem(self.horizSpacer3)
        self.controlButtonLayout.addWidget(self.downloadButton)

        #add items to verticalMainLayout->listButtonLayout
        self.listButtonLayout.addWidget(self.prevButton)
        self.listButtonLayout.addSpacerItem(self.horizSpacer1)
        self.listButtonLayout.addWidget(self.nextButton)
        self.listButtonLayout.addSpacerItem(self.horizSpacer2)
    
    def showPicture(self, path):
        self.path = path
        self.image = QPixmap(self.path)
        self.updateImage()
    
    def updateImage(self):
        if self.path:
            img_size = QSize(self.width() - self.width()*0.1, self.height() - self.height()*0.2)
            self.imageLabel.setPixmap(self.image.scaled(img_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateImage()