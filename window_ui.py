# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_e6reader(object):
    def setupUi(self, e6reader):
        if not e6reader.objectName():
            e6reader.setObjectName(u"e6reader")
        e6reader.resize(1129, 596)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(e6reader.sizePolicy().hasHeightForWidth())
        e6reader.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(e6reader)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1081, 541))
        self.MainLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.MainLayout.setObjectName(u"MainLayout")
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.searchLayout = QHBoxLayout()
        self.searchLayout.setObjectName(u"searchLayout")
        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)

        self.searchLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)

        self.searchLayout.addWidget(self.pushButton)


        self.MainLayout.addLayout(self.searchLayout)

        self.scrollArea = QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidgetImg = QWidget()
        self.scrollWidgetImg.setObjectName(u"scrollWidgetImg")
        self.scrollWidgetImg.setGeometry(QRect(0, 0, 1075, 493))
        self.scrollArea.setWidget(self.scrollWidgetImg)

        self.MainLayout.addWidget(self.scrollArea)

        e6reader.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(e6reader)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1129, 30))
        e6reader.setMenuBar(self.menubar)

        self.retranslateUi(e6reader)

        QMetaObject.connectSlotsByName(e6reader)
    # setupUi

    def retranslateUi(self, e6reader):
        e6reader.setWindowTitle(QCoreApplication.translate("e6reader", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("e6reader", u"Search", None))
    # retranslateUi

