from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/group_table_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GroupTableWidget(Base, Form):
    def __init__(self, parent = None):
        super(GroupTableWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, cohort):
        self.cohort = cohort
        self.init_table()
        self.init_buttons()

    def init_table(self):
        self.tableWidget_groups.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_groups.itemSelectionChanged.connect(self.update_group_operation_buttons)
        self.tableWidget_groups.cellChanged.connect(self.cell_changed_in_group_table)

        header = self.tableWidget_groups.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        self.tableWidget_groups.setColumnWidth(0, 100)
        self.tableWidget_groups.setColumnWidth(1, 150)
        self.tableWidget_groups.setColumnWidth(2, 150)

    def init_buttons(self):
        self.btnLoadSubject.clicked.connect(self.load_subject_group)

        self.btnAdd.clicked.connect(self.add_group)
        self.btnRemove.clicked.connect(self.remove_group)
        self.btnMoveUp.clicked.connect(self.move_group_up)
        self.btnMoveDown.clicked.connect(self.move_group_down)

        self.btnInvert.clicked.connect(self.invert_group)
        self.btnMerge.clicked.connect(self.merge_groups)
        self.btnIntersect.clicked.connect(self.intersect_groups)

    def set_callback(self, callback_function):
        self.update_callback_function = callback_function

    def update(self, selected = None):
        if self.update_callback_function:
            self.update_callback_function()
        self.update_table(selected)

    def update_group_operation_buttons(self):
        checked_groups = len(self.get_selected())
        self.btnInvert.setEnabled(checked_groups > 0)
        self.btnMerge.setEnabled(checked_groups > 1)
        self.btnIntersect.setEnabled(checked_groups > 1)
        self.update()

    def update_table(self, selected_groups = None):
        if np.any(selected_groups == None):
            selected_groups = self.get_selected()
        self.tableWidget_groups.blockSignals(True)
        self.tableWidget_groups.clearContents()
        self.tableWidget_groups.setRowCount(0)

        for i in range(len(self.cohort.groups)):
            self.tableWidget_groups.setRowCount(i+1)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)

            item = QTableWidgetItem(self.cohort.groups[i].name)
            self.tableWidget_groups.setItem(i, 0, item)

            item = QTableWidgetItem(str(len(self.cohort.groups[i].subjects)))
            self.tableWidget_groups.setItem(i, 1, item)

            item = QTableWidgetItem(self.cohort.groups[i].description)
            self.tableWidget_groups.setItem(i, 2, item)

        self.set_selected(selected_groups)
        self.tableWidget_groups.blockSignals(False)

    def cell_changed_in_group_table(self, row, column):
        if column == 0: # name
            self.cohort.groups[row].name = self.tableWidget_groups.item(row, column).text()
        elif column == 2: # notes
            self.cohort.groups[row].description = self.tableWidget_groups.item(row, column).text()
        self.update()

    def load_subject_group(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","Subject files (*.txt *.xml *.xlsx);; \
                                                                                               Text files (*.txt);; \
                                                                                               XML files (*.xml);; \
                                                                                               XLSX files (*.xlsx)", options=options)
        for file_name in file_names:
            extension = file_name.split(".")[-1]
            if extension == "txt":
                self.cohort.load_from_txt(file_name)
            elif extension == "xml":
                self.cohort.load_from_xml(file_name)
            elif extension == "xlsx":
                self.cohort.load_from_xlsx(file_name)
        if len(file_names) > 0:
            self.update()

    def get_selected(self):
        rows = [item.row() for item in self.tableWidget_groups.selectionModel().selectedRows()]
        return np.array(rows)

    def set_selected(self, selected):
        mode = self.tableWidget_groups.selectionMode()
        self.tableWidget_groups.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in selected:
            self.tableWidget_groups.selectRow(row)
        self.tableWidget_groups.setSelectionMode(mode)

    def add_group(self):
        self.cohort.add_group()
        self.update(self.get_selected())

    def remove_group(self):
        selected_groups = self.cohort.remove_groups(self.get_selected())
        self.update(selected_groups)

    def move_group_up(self):
        selected_groups = self.cohort.move_up_groups(self.get_selected())
        self.update(selected_groups)

    def move_group_down(self):
        selected_groups = self.cohort.move_down_groups(self.get_selected())
        self.update(selected_groups)

    def invert_group(self):
        self.cohort.invert_groups(self.get_selected())
        self.update(self.get_selected())

    def merge_groups(self):
        self.cohort.merge_groups(self.get_selected())
        self.update(self.get_selected())

    def intersect_groups(self):
        self.cohort.intersect_groups(self.get_selected())
        self.update(self.get_selected())


