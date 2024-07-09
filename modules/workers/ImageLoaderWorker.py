from ..workers.WorkerSignals import WorkerSignals

from PySide6.QtCore import QRunnable
from urllib.request import urlretrieve
from pathlib import Path

class ImageLoaderWorker(QRunnable):
    def __init__(self, sample, widget):
        super().__init__()
        self.sample = sample
        self.widget = widget
        self.signals = WorkerSignals()
    
    def run(self):
        try:
            md5 = self.sample["file"]["md5"]
            img_path = f'./cache/{md5}.{self.sample["file"]["ext"]}'
            if Path(img_path).exists():
                print(f'Preview ({md5}) already exists (cache)')
                self.signals.image_loaded.emit(img_path, self.widget)
            else:
                try:
                    print(f'Downloading preview... ({md5[5:]}...)')
                    urlretrieve(self.sample['sample']['url'], img_path)
                    print(f'Downloaded successfully!... ({md5[5:]}...)')
                except Exception as err:
                    self.signals.error.emit(str(err))
                self.signals.image_loaded.emit(img_path, self.widget)
        except Exception as err:
            self.signals.error.emit(str(err))