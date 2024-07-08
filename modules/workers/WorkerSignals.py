from PySide6.QtCore import QObject, Signal

class WorkerSignals(QObject):
    result = Signal(object)
    error = Signal(str)
    image_loaded = Signal(object)