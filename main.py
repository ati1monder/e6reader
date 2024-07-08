from appwindow import AppWindow

import sys
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('e6reader')

    appw = AppWindow()
    appw.show()

    app.exec()