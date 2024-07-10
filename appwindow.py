from modules import var
from modules.ui_form import ImagePixmapLabel, FlowLayout, LoadingAnimation, InfoImageBox, ImageWindow
from modules.workers import FetchPageWorker, ImageLoaderWorker
from window import Ui_e6reader

from PySide6.QtWidgets import QMainWindow, QSizePolicy, QSizePolicy
from PySide6.QtCore import Slot, QThreadPool, Qt
from functools import partial

class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.ui = Ui_e6reader()
        self.ui.setupUi(self)
        self.setWindowTitle('e6reader')

        self.ui.pushButton.clicked.connect(self.get_images_api)
        self.ui.lineEdit.returnPressed.connect(self.get_images_api)

        self.ui.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.scrollArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.threadpool = QThreadPool()
        
        self.imgLayout = FlowLayout(self.ui.scrollWidgetImg, margin=10, hSpacing=10, vSpacing=10)

        self.loadAnim = LoadingAnimation(self.ui.scrollArea)

    @Slot()
    def get_images_api(self):
        self.loadAnim.start()
        self.imgLayout.clearlayout()
        worker = FetchPageWorker(url=var.url, page=1, tags=self.ui.lineEdit.text().replace(' ', '+'), username=var.username, api=var.api)
        worker.signals.result.connect(self.handle_result)
        worker.signals.error.connect(self.handle_error)
        self.threadpool.start(worker)

    @Slot(str, object)
    def preview_loaded(self, path: str, image_label: ImagePixmapLabel):
        image_label.addImage(path)
        image_label.clicked.connect(self.photo_window)
    
    @Slot()
    def photo_window(self):
        self.iteration_item = 1
        print(self.imgLayout.items.index(self.sender().parent().object))
        sample = self.sender().parent()
        self.test_window = ImageWindow()
        self.test_window.show()
        image_loader = ImageLoaderWorker(sample.info, 'image', self.test_window)
        image_loader.signals.image_loaded.connect(self.image_loaded)
        self.threadpool.start(image_loader)

        self.test_window.nextButton.clicked.connect(partial(self.list_pictures, ('next', sample)))
        self.test_window.prevButton.clicked.connect(partial(self.list_pictures, ('prev', sample)))
    
    @Slot()
    def list_pictures(self, data):
        name, sender = data
        current_index = self.imgLayout.items.index(sender.object)
        current_item = None

        if name == 'next':
            current_item = self.imgLayout.items[current_index+self.iteration_item]
            self.iteration_item = self.iteration_item + 1
        elif name == 'prev':
            current_item = self.imgLayout.items[current_index-1]
            self.iteration_item = self.iteration_item - 1
        
        image_loader = ImageLoaderWorker(current_item.parent().info, 'image', self.test_window)
        image_loader.signals.image_loaded.connect(self.image_loaded)
        self.threadpool.start(image_loader)
        self.sample = current_item.parent()
        

    @Slot(str, object)
    def image_loaded(self, path, widget: ImageWindow):
        widget.showPicture(path)

    @Slot(object)
    def handle_result(self, result):
        self.loadAnim.stop()
        self.imgLayout.clearlayout()

        for sample in result:
            image_label = ImagePixmapLabel()
            image_box = InfoImageBox(image_label, sample)
            self.imgLayout.addWidget(image_box)
            self.imgLayout.itemAppend(image_label)

            img_loader_worker = ImageLoaderWorker(sample, 'preview', image_label)
            img_loader_worker.signals.preview_loaded.connect(self.preview_loaded)
            img_loader_worker.signals.error.connect(self.handle_error)
            self.threadpool.start(img_loader_worker)
            
    @Slot(str)
    def handle_error(self, error):
        print(error)
    
    def resizeEvent(self, event):
        self.ui.scrollArea.setFixedSize(self.width(), self.height() - self.ui.lineEdit.height())

        QMainWindow.resizeEvent(self, event)