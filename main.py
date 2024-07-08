from modules import var
from modules.ui_form import ImagePixmapLabel, FlowLayout
from modules.workers import FetchPageWorker, ImageLoaderWorker
from window import Ui_e6reader

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Slot, QThreadPool
from PySide6.QtGui import Qt

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = Ui_e6reader()
        self.ui.setupUi(self)
        self.setWindowTitle('e6reader')

        self.item_width = 150

        self.ui.pushButton.clicked.connect(self.get_images_api)
        self.ui.lineEdit.returnPressed.connect(self.get_images_api)

        self.threadpool = QThreadPool()

        self.imgLayout = FlowLayout(self.ui.scrollWidgetImg, margin=10, hSpacing=10, vSpacing=10)

    @Slot()
    def get_images_api(self):
        # self.imgLayout.clearlayout()
        worker = FetchPageWorker(url=var.url, page=1, tags=self.ui.lineEdit.text().replace(' ', '+'), username=var.username, api=var.api)
        worker.signals.result.connect(self.handle_result)
        worker.signals.error.connect(self.handle_error)
        self.threadpool.start(worker)

    @Slot(object)
    def image_loaded(self, data):
        path, row, col = data

        image_label = ImagePixmapLabel()
        image_label.appendImage(path)

        # self.imgLayout.addWidget(image_label, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
        self.imgLayout.addWidget(image_label)
        image_label.clicked.connect(self.test_func)
    
    @Slot()
    def test_func(self):
        print(self.Image_List)

    @Slot(object)
    def handle_result(self, result):
        # self.imgLayout.clearlayout()

        available_width = self.width()
        cols = max(1, available_width // self.item_width)

        for index, sample in enumerate(result):
            row = index // cols
            col = index % cols
            img_loader_worker = ImageLoaderWorker(sample, row, col)
            img_loader_worker.signals.image_loaded.connect(self.image_loaded)
            img_loader_worker.signals.error.connect(self.handle_error)
            self.threadpool.start(img_loader_worker)
            
    @Slot(str)
    def handle_error(self, error):
        print(error)
    
    def resizeEvent(self, event):
        self.ui.scrollArea.setFixedSize(self.width(), self.height() - 30)

        QMainWindow.resizeEvent(self, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('e6reader')

    appw = AppWindow()
    appw.show()

    app.exec()