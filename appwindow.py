from modules import var
from modules.ui_form import ImagePixmapLabel, FlowLayout, LoadingAnimation, InfoImageBox, ImageWindow
from modules.workers import FetchPageWorker, ImageLoaderWorker
from window import Ui_e6reader

from PySide6.QtWidgets import QMainWindow, QSizePolicy, QSizePolicy
from PySide6.QtCore import Slot, QThreadPool, Qt

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
        image_label.clicked.connect(self.test_func)
    
    @Slot()
    def test_func(self):
        sample = self.sender().parent().info
        self.test_window = ImageWindow()
        self.test_window.show()
        image_loader = ImageLoaderWorker(sample, 'image', self.test_window)
        image_loader.signals.image_loaded.connect(self.image_loaded)
        self.threadpool.start(image_loader)

    @Slot(str, object)
    def image_loaded(self, path, widget: ImageWindow):
        print('working!')
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