import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI

ui_file = abs_path_from_relative(__file__, "../ui_files/group_table_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GroupTableWidget(Base, Form):
    def __init__(self, parent = None):
        super(GroupTableWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_table()
        self.init_buttons()
        self.read_only = False

    def init(self, cohort):
        self.cohort = cohort
        if self.cohort.subject_class.structural():
            self.btnLoadFolder.hide()

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
        self.btnLoadFolder.clicked.connect(self.load_subject_folder)

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
        if not self.read_only:
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
        self.tableWidget_groups.setRowCount(len(self.cohort.groups))

        for i in range(len(self.cohort.groups)):
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setAlignment(QtCore.Qt.AlignHCenter)

            item = QTableWidgetItem(self.cohort.groups[i].name)
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget_groups.setItem(i, 0, item)

            item = QTableWidgetItem(str(len(self.cohort.groups[i].subjects)))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget_groups.setItem(i, 1, item)

            item = QTableWidgetItem(self.cohort.groups[i].description)
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget_groups.setItem(i, 2, item)

        self.set_selected(selected_groups)
        self.tableWidget_groups.blockSignals(False)

    def cell_changed_in_group_table(self, row, column):
        if column == 0: # name
            self.cohort.groups[row].name = self.tableWidget_groups.item(row, column).text()
        elif column == 2: # notes
            self.cohort.groups[row].description = self.tableWidget_groups.item(row, column).text()
        self.update()

    def load_subject_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self,"Load subject folder", "", options = options)
        if not folder:
            return
        duplicates = False
        warning = False
        try:
            duplicates, warning = self.cohort.load_from_folder(folder)
        except Exception as e:
            self.load_file_error(str(e))
        if duplicates:
            self.load_file_warning("The selected file contains some subjects that are already loaded. These were skipped.")
        if warning:
            self.load_file_warning("Some files could not be loaded.")
        self.update()

    def load_subject_group(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self,"Load subject group", "",
                                                     "Subject files (*.txt *.xml *.xlsx);; \
                                                     Text files (*.txt);; \
                                                     XML files (*.xml);; \
                                                     XLSX files (*.xlsx)", options = options)
        duplicates = False
        try:
            for file_name in file_names:
                extension = file_name.split(".")[-1]
                if extension == "txt":
                    duplicates = self.cohort.load_from_txt(file_name)
                elif extension == "xml":
                    duplicates = self.cohort.load_from_xml(file_name)
                elif extension == "xlsx":
                    duplicates = self.cohort.load_from_xlsx(file_name)
        except Exception as e:
            self.load_file_error(str(e))
        if duplicates:
            self.load_file_warning("The selected file contains some subjects that are already loaded. These were skipped.")
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
        self.update_group_operation_buttons()

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

    def set_read_only(self):
        self.read_only = True
        locked_items = [self.btnLoadSubject, self.btnAdd, self.btnRemove, self.btnMoveUp,
                        self.btnMoveDown, self.btnInvert, self.btnMerge, self.btnIntersect]
        for item in locked_items:
            item.setEnabled(False)
        self.update_table()

    def load_file_error(self, exception):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(str(exception))
        msg_box.setWindowTitle("Import error")
        msg_box.exec_()

    def load_file_warning(self, string):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(string)
        msg_box.setWindowTitle("Import warning")
        msg_box.exec_()


