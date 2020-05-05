from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.cohort.subjects import *

ui_file = abs_path_from_relative(__file__, "../ui_files/subject_data_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class SubjectDataWidget(Base, Form):
    def __init__(self, parent = None):
        super(SubjectDataWidget, self).__init__(parent)
        self.setupUi(self)
        self.initialized = False
        self.read_only = False

    def init(self, cohort):
        self.cohort = cohort
        if not self.initialized:
            self.init_table()
            self.init_buttons()
            self.initialized = True

    def init_table(self):
        if self.cohort.subject_class == SubjectfMRI:
            self.listSubjects.currentRowChanged.connect(self.subject_list_row_changed)
            self.selected_subject = None
        else: #MRI
            self.listSubjects.hide()
            self.labelSubjects.hide()
            self.btnAddRow.hide()
            self.btnRemoveRow.hide()

        self.tableWidget.setItemDelegate(FloatDelegate(self.tableWidget))
        self.tableWidget.cellChanged.connect(self.cell_changed_in_table)

    def init_buttons(self):
        self.btnSaveSubjectsTxt.clicked.connect(lambda signal, file_type = 'txt', save_to_function = self.cohort.save_to_txt: self.save_subjects(file_type, save_to_function))
        self.btnSaveSubjectsXlsx.clicked.connect(lambda signal, file_type = 'xlsx', save_to_function = self.cohort.save_to_xlsx: self.save_subjects(file_type, save_to_function))
        self.btnAddRow.clicked.connect(self.add_row)
        self.btnRemoveRow.clicked.connect(self.remove_row)

    def save_subjects(self, file_type, save_to_function):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if self.cohort.subject_class == SubjectMRI:
            file_name, name = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()",
                                                        "subjects.{}".format(file_type),
                                                        "{} files (*.{})".format(file_type, file_type),
                                                        options = options)
        elif self.cohort.subject_class == SubjectfMRI:
            file_name = QFileDialog.getExistingDirectory(self, "Open directory", " ", options = options)
        if file_name:
            save_to_function(file_name)

    def set_callback(self, callback_function):
        self.update_callback_function = callback_function

    def update(self):
        if self.update_callback_function:
            self.update_callback_function()
        self.update_table()

    def cell_changed_in_table(self, row, column):
        new_value = float(self.tableWidget.item(row, column).text())
        if self.cohort.subject_class == SubjectMRI:
            self.cohort.subjects[row].data_dict['data'].value[column] = new_value
        else:
            self.selected_subject.data_dict['data'].value[row, column] = new_value
        self.update()

    def update_table(self):
        if self.cohort.subject_class == SubjectMRI:
            self.update_table_structural()
        else:
            self.update_subject_list()

    def update_table_functional(self):
        self.tableWidget.blockSignals(True)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # Update columns:
        self.tableWidget.setColumnCount(len(self.cohort.atlas.get_brain_region_labels()))
        for i, label in enumerate(self.cohort.atlas.get_brain_region_labels()):
            item = QTableWidgetItem(label)
            self.tableWidget.setHorizontalHeaderItem(i, item)

        # Update subject:
        data = self.selected_subject.data_dict['data'].value
        self.tableWidget.setRowCount(data.shape[0])
        for (i, j), value in np.ndenumerate(data):
            item = QTableWidgetItem(float_to_string(value))
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, j, item)
        self.tableWidget.blockSignals(False)

    def update_table_structural(self):
        self.tableWidget.blockSignals(True)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        #Update columns:
        self.tableWidget.setColumnCount(len(self.cohort.atlas.brain_regions))
        for i, label in enumerate(self.cohort.atlas.get_brain_region_labels()):
            item = QTableWidgetItem(label)
            self.tableWidget.setHorizontalHeaderItem(i, item)

        # Update subjects:
        self.tableWidget.setRowCount(len(self.cohort.subjects))
        for i in range(len(self.cohort.subjects)):
            item = QTableWidgetItem(self.cohort.subjects[i].id)
            self.tableWidget.setVerticalHeaderItem(i, item)
            for j in range(len(self.cohort.subjects[i].data_dict['data'].value)):
                value = float_to_string(self.cohort.subjects[i].data_dict['data'].value[j])
                item = QTableWidgetItem(value)
                if self.read_only:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, j, item)

        self.tableWidget.blockSignals(False)

    def update_subject_list(self):
        self.listSubjects.blockSignals(True)
        self.listSubjects.clear()
        select_row = 0
        for i, subject in enumerate(self.cohort.subjects):
            if subject == self.selected_subject:
                select_row = i
            item = QListWidgetItem(subject.id)
            self.listSubjects.addItem(item)
        self.listSubjects.blockSignals(False)
        if len(self.cohort.subjects) > 0:
            self.listSubjects.setCurrentRow(select_row)

    def subject_list_row_changed(self, row):
        self.selected_subject = self.cohort.subjects[row]
        self.update_table_functional()

    def add_row(self):
        self.selected_subject.data_dict['data'].add_row()
        self.update_table_functional()

    def remove_row(self):
        self.selected_subject.data_dict['data'].remove_row()
        self.update_table_functional()

    def set_read_only(self):
        self.read_only = True
        self.update_table()
