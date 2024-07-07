from modules import e6post, var
from urllib.request import urlretrieve
from window import Ui_e6reader

import sys
from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QLabel, QFrame
from PySide6.QtCore import Slot, QThreadPool, QRunnable, Signal, QObject, SIGNAL
from PySide6.QtGui import QPixmap, Qt

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = Ui_e6reader()
        self.ui.setupUi(self)
        self.setWindowTitle('e6reader')

        self.item_width = 150

        self.ui.pushButton.clicked.connect(self.get_images)
        self.ui.lineEdit.returnPressed.connect(self.get_images)

        self.threadpool = QThreadPool()

        self.imgGridLayout = QGridLayout(self.ui.scrollWidgetImg)
    
    def clearlayout(self, layout):
        for i in range(layout.count()): 
            self.imgGridLayout.itemAt(i).widget().deleteLater()

    @Slot()
    def get_images(self):
        self.clearlayout(self.imgGridLayout)
        worker = FetchPageWorker(url=var.url, page=1, tags=self.ui.lineEdit.text().replace(' ', '+'), username=var.username, api=var.api)
        worker.signals.result.connect(self.handle_result)
        worker.signals.error.connect(self.handle_error)
        self.threadpool.start(worker)

    @Slot(object)
    def image_loaded(self, data):
        path, row, col = data
        image = QPixmap(path).scaled(self.item_width, self.item_width, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        image_label = ClickableLabel()
        image_label.setFixedSize(self.item_width, self.item_width)
        image_label.setPixmap(image)

        self.imgGridLayout.addWidget(image_label, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
        image_label.clicked.connect(self.test_func)
    
    @Slot()
    def test_func(self):
        print('a!')
    
    @Slot(object)
    def handle_result(self, result):
        self.clearlayout(self.imgGridLayout)

        available_width = self.width()
        cols = max(1, available_width // self.item_width)

        for index, sample in enumerate(result):
            row = index // cols
            col = index % cols
            print(sample['sample']['url'])
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

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    image_loaded = Signal(object)

class ImageLoaderWorker(QRunnable):
    def __init__(self, sample, row, col):
        super().__init__()
        self.sample = sample
        self.row = row
        self.col = col
        self.signals = WorkerSignals()
    
    def run(self):
        try:
            img_path = f'./cache/{self.sample["file"]["md5"]}.{self.sample["file"]["ext"]}'
            urlretrieve(self.sample['sample']['url'], img_path)
            self.signals.image_loaded.emit((img_path, self.row, self.col))
        except Exception as err:
            self.signals.error.emit(str(err))

class FetchPageWorker(QRunnable):
    def __init__(self, url, page, tags, username, api):
        super().__init__()
        self.url = url
        self.page = page
        self.tags = tags
        self.username = username
        self.api = api
        self.res = []
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = e6post.fetch_page(url=self.url, page=self.page, tags=self.tags, username=self.username, api=self.api)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('e6reader')

    appw = AppWindow()
    appw.show()

    app.exec()