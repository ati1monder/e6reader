from ..workers.WorkerSignals import WorkerSignals

from PySide6.QtCore import QRunnable
from urllib.request import urlretrieve
from pathlib import Path

class ImageLoaderWorker(QRunnable):
    def __init__(self, sample, widget):
        super().__init__()
        self.sample = sample
        self.widget = widget
        self.md5 = self.sample["file"]["md5"]
        self.img_path = f'./cache/{self.md5}.{self.sample["file"]["ext"]}'
        self.signals = WorkerSignals()

    def emit_signal(self):
        self.signals.image_loaded.emit(self.img_path, self.widget)

    def download(self):
        if Path(self.img_path).exists():
            print(f'Preview ({self.md5}) already exists (cache)')
            self.emit_signal()
        else:
            print(f'Downloading preview... ({self.md5[5:]}...)')
            urlretrieve(self.sample['sample']['url'], self.img_path)
            print(f'Downloaded successfully!... ({self.md5[5:]}...)')
            self.emit_signal()
    
    def run(self):
        try:
            self.download()
        except Exception as err:
            self.signals.error.emit(str(err))