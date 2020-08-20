from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.file_utility import abs_path_from_relative
from braphy.utility.qt_utility import IntDelegate

ui_file = abs_path_from_relative(__file__, "../ui_files/groups_and_demographics_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GroupsAndDemographicsWidget(Base, Form):
    def __init__(self, parent = None):
        super(GroupsAndDemographicsWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_table()
        self.init_buttons()

        self.subject_check_boxes = []
        self.subject_in_group_check_boxes = {}
        self.read_only = False

    def init(self, cohort):
        self.cohort = cohort

    def init_table(self):
        self.tableWidget.setItemDelegateForColumn(2, IntDelegate(self.tableWidget))
        self.tableWidget.cellChanged.connect(self.cell_changed_in_table)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.select_all)
        self.btnClearSelection.clicked.connect(self.clear_selection)
        self.btnAddSubject.clicked.connect(self.add_subject)
        self.btnAddAbove.clicked.connect(self.add_subjects_above)
        self.btnAddBelow.clicked.connect(self.add_subjects_below)
        self.btnRemove2.clicked.connect(self.remove_subjects)
        self.btnMoveUp2.clicked.connect(self.move_subjects_up)
        self.btnMoveDown2.clicked.connect(self.move_subjects_down)
        self.btnMoveToTop.clicked.connect(self.move_subjects_to_top)
        self.btnMoveToBottom.clicked.connect(self.move_subjects_to_bottom)
        self.btnNewGroup.clicked.connect(self.new_group_from_selected)

    def set_callback(self, callback_function):
        self.update_callback_function = callback_function

    def update(self, selected = None):
        if self.update_callback_function:
            self.update_callback_function()
        self.update_table(selected)

    def cell_changed_in_table(self, row, column):
        if column == 0: # check box
            pass
        elif column == 1: # subject code
            self.cohort.subjects[row].id = self.tableWidget.item(row, column).text()
        else: # scalar data
            column_header = self.tableWidget.horizontalHeaderItem(column).text()
            new_value = float(self.tableWidget.item(row, column).text())
            self.cohort.subjects[row].data_dict[column_header].value = new_value
        self.update()

    def update_table(self, selected = None):
        if np.any(selected == None):
            selected = self.get_selected()

        self.tableWidget.blockSignals(True)
        self.tableWidget.clear_table()
        self.subject_in_group_check_boxes = {}

        #Update columns:
        self.tableWidget.setColumnCount(1)
        item = QTableWidgetItem('Subject Code')
        self.tableWidget.setHorizontalHeaderItem(0, item)
        try:
            keys = list(self.cohort.subjects[0].data_dict.keys())
        except:
            keys = []
        for i in range(len(keys)):
            if keys[i] == 'data':
                continue
            item = QTableWidgetItem(keys[i])
            self.tableWidget.setColumnCount(i+2)
            self.tableWidget.setHorizontalHeaderItem(i+1, item)

        nbr_columns = self.tableWidget.columnCount()
        for i in range(len(self.cohort.groups)):
            item = QTableWidgetItem(self.cohort.groups[i].name)
            self.tableWidget.setColumnCount(nbr_columns+i+1)
            self.tableWidget.setHorizontalHeaderItem(nbr_columns+i, item)
            self.subject_in_group_check_boxes[self.cohort.groups[i]] = []

        # Update subjects:
        for i in range(len(self.cohort.subjects)):
            self.tableWidget.setRowCount(i+1)

            item = QTableWidgetItem(self.cohort.subjects[i].id)
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 0, item)

            for j in range(len(keys)):
                if keys[j] == 'data':
                    continue
                item = QTableWidgetItem(str(self.cohort.subjects[i].data_dict[keys[j]].value))
                if self.read_only:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, j+1, item)

            for j in range(len(self.cohort.groups)):
                widget = QWidget()
                layout = QHBoxLayout()
                layout.setAlignment(QtCore.Qt.AlignHCenter)
                check_box = QCheckBox()
                check_box.i = i
                check_box.j = j
                if self.read_only:
                    check_box.setEnabled(False)
                self.subject_in_group_check_boxes[self.cohort.groups[j]].append(check_box)
                self.subject_in_group_check_boxes[self.cohort.groups[j]][i].stateChanged.connect(self.subject_in_group_check_box_changed)
                if self.cohort.subjects[i] in self.cohort.groups[j].subjects:
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].blockSignals(True)
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].setChecked(True)
                    self.subject_in_group_check_boxes[self.cohort.groups[j]][i].blockSignals(False)
                layout.addWidget(self.subject_in_group_check_boxes[self.cohort.groups[j]][i])
                widget.setLayout(layout)
                self.tableWidget.setCellWidget(i, nbr_columns+j, widget)

        self.set_selected(selected)
        self.tableWidget.blockSignals(False)

    def subject_in_group_check_box_changed(self):
        check_box = self.sender()
        if check_box.isChecked():
            self.cohort.groups[check_box.j].add_subject(self.cohort.subjects[check_box.i])
        else:
            self.cohort.groups[check_box.j].remove_subject(self.cohort.subjects[check_box.i])
        self.update()

    def get_selected(self):
        return self.tableWidget.get_selected()

    def set_selected(self, selected):
        self.tableWidget.set_selected(selected)

    def select_all(self):
        self.tableWidget.selectAll()

    def clear_selection(self):
        self.tableWidget.clearSelection()

    def add_subject(self):
        self.cohort.add_subject()
        self.update()

    def add_subjects_above(self):
        selected_subjects = self.get_selected()
        selected_subjects, added_subjects = self.cohort.add_above_subjects(selected_subjects)
        self.update(selected_subjects)

    def add_subjects_below(self):
        selected_subjects = self.get_selected()
        selected_subjects, added_subjects = self.cohort.add_below_subjects(selected_subjects)
        self.update(selected_subjects)

    def remove_subjects(self):
        selected_subjects = self.get_selected()
        self.cohort.remove_subjects_from_all_groups(selected_subjects)
        selected_subjects = self.cohort.remove_subjects(selected_subjects)
        self.update(selected_subjects)

    def move_subjects_up(self):
        selected_subjects = self.get_selected()
        selected_subjects = self.cohort.move_up_subjects(selected_subjects)
        self.update(selected_subjects)

    def move_subjects_down(self):
        selected_subjects = self.get_selected()
        selected_subjects = self.cohort.move_down_subjects(selected_subjects)
        self.update(selected_subjects)

    def move_subjects_to_top(self):
        selected_subjects = self.get_selected()
        selected_subjects = self.cohort.move_to_top_subjects(selected_subjects)
        self.update(selected_subjects)

    def move_subjects_to_bottom(self):
        selected_subjects = self.get_selected()
        selected_subjects = self.cohort.move_to_bottom_subjects(selected_subjects)
        self.update(selected_subjects)

    def new_group_from_selected(self):
        selected_subjects = self.get_selected()
        self.cohort.new_group_from_selected(selected_subjects)
        self.update()

    def set_read_only(self):
        self.read_only = True
        locked_items = [self.btnSelectAll, self.btnClearSelection, self.btnAddSubject,
                        self.btnAddAbove, self.btnAddBelow, self.btnRemove2, self.btnMoveUp2,
                        self.btnMoveDown2, self.btnMoveToTop, self.btnMoveToBottom, self.btnNewGroup]
        for item in locked_items:
            item.setEnabled(False)
        self.update_table()

