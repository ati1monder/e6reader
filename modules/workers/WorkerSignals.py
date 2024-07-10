from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    preview_loaded = Signal(str, object)
    image_loaded = Signal(str, object)