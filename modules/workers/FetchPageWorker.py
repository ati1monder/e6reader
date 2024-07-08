from .. import e6post

from PySide6.QtCore import QRunnable
from ..workers.WorkerSignals import WorkerSignals

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