from .WorkerSignals import WorkerSignals

from PySide6.QtCore import QRunnable
from urllib.request import urlretrieve
from pathlib import Path

class ImageLoaderWorker(QRunnable):
    def __init__(self, sample, method, widget = None):
        super().__init__()
        self.sample = sample
        self.widget = widget
        self.method = method
        self.md5 = self.sample["file"]["md5"]
        self.img_path = f'./cache/{self.method + self.md5}.{self.sample["file"]["ext"]}'
        self.signals = WorkerSignals()

    def emit_signal(self):
        match self.method:
            case 'preview':
                self.signals.preview_loaded.emit(self.img_path, self.widget)
            case 'image':
                self.signals.image_loaded.emit(self.img_path, self.widget)

    def download(self):
        match self.method:
            case 'preview':
                url = self.sample['sample']['url']
            case 'image':
                url = self.sample['file']['url']

        if Path(self.img_path).exists():
            print(f'Preview ({self.method + self.md5}) already exists (cache)')
            self.emit_signal()
        else:
            print(f'Downloading preview... (sample_{self.md5[5:]}...)')
            urlretrieve(url, self.img_path)
            print(f'Downloaded successfully!... ({self.md5[5:]}...)')
            self.emit_signal()
    
    def run(self):
        print('runs')
        try:
            self.download()
        except Exception as err:
            self.signals.error.emit(str(err))