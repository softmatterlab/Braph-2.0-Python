from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
import numpy as np

class TableManager(QTableWidget):
    def __init__(self, parent):
        super().__init__()

    def get_selected(self):
        rows = [item.row() for item in self.selectionModel().selectedRows()]
        return np.array(rows)

    def set_selected(self, selected):
        self.clearSelection()
        mode = self.selectionMode()
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in selected:
            self.selectRow(row)
        self.setSelectionMode(mode)

    def clear_table(self, row_count = 0):
        self.clearContents()
        self.setRowCount(row_count)