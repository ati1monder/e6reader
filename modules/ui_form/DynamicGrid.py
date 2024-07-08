from PySide6.QtWidgets import QGridLayout

class DynamicGrid(QGridLayout):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.gridlist = []
    
    def clearlayout(self):
        for i in reversed(range(self.count())):
            widget = self.itemAt(i).widget()
            if widget:
                widget.deleteLater()
    
    def appendItem(self, item):
        self.gridlist.append(item)
    
    def count(self):
        return len(self.gridlist)