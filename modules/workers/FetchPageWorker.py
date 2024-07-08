from .. import e6post

from PySide6.QtCore import QRunnable
from ..workers.WorkerSignals import WorkerSignals

class FetchPageWorker(QRunnable):
    def __init__(self, url, tags, username, api):
        super().__init__()
        self.url = url
        self.tags = tags
        self.username = username
        self.api = api
        self.res = []
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = e6post.fetch_all(url=self.url, tags=self.tags, username=self.username, api=self.api)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))