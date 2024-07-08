from ..workers.WorkerSignals import WorkerSignals

from PySide6.QtCore import QRunnable
from urllib.request import urlretrieve

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