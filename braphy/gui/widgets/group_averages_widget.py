from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.cohort.subjects import *

ui_file = abs_path_from_relative(__file__, "../ui_files/group_averages_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GroupAveragesWidget(Base, Form):
    def __init__(self, cohort, parent = None):
        super(GroupAveragesWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, cohort):
        self.cohort = cohort
        self.spinBoxPermutations.valueChanged.connect(self.comparison)
        self.btnExportTxt.clicked.connect(self.export_as_txt)
        self.btnExportTxt.setEnabled(False)
        self.button_group = QtWidgets.QButtonGroup(self)

    def set_callback(self, callback_function):
        self.update_callback_function = callback_function

    def update(self, selected = None):
        if self.update_callback_function:
            self.update_callback_function()
        self.update_tables(selected)

    def update_tables(self):
        self.update_averages_table()
        self.update_selection_table()

    def update_averages_table(self):
        self.tableWidget_averages.setColumnCount(len(self.cohort.atlas.brain_regions))
        self.tableWidget_averages.setHorizontalHeaderLabels(self.cohort.atlas.get_brain_region_labels())
        self.tableWidget_averages.setRowCount(len(self.cohort.groups)*2)
        for i, group in enumerate(self.cohort.groups):
            item = QTableWidgetItem("Average {}".format(group.name))
            self.tableWidget_averages.setVerticalHeaderItem((2*i), item)
            averages = group.averages()
            for j in range(len(averages)):
                item = QTableWidgetItem(str(averages[j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget_averages.setItem(2*i, j, item)

            item = QTableWidgetItem("Std {}".format(group.name))
            self.tableWidget_averages.setVerticalHeaderItem((2*i+1), item)
            stds = group.standard_deviations()
            for j in range(len(stds)):
                item = QTableWidgetItem(str(stds[j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget_averages.setItem(2*i+1, j, item)

    def update_selection_table(self):
        self.tableWidget_comparison.setColumnCount(len(self.cohort.atlas.brain_regions))
        self.tableWidget_comparison.setHorizontalHeaderLabels(self.cohort.atlas.get_brain_region_labels())

        self.tableWidget_selection.blockSignals(True)
        group_button = self.button_group.checkedButton()
        if group_button:
            group_1 = group_button.group1
            group_2 = group_button.group2
            selected_groups = [group_1, group_2]
        else:
            selected_groups = [None, None]
        self.tableWidget_selection.clearContents()

        group_names = [group.name for group in self.cohort.groups]
        self.tableWidget_selection.setRowCount(len(group_names))
        self.tableWidget_selection.setColumnCount(len(group_names))
        self.tableWidget_selection.setVerticalHeaderLabels(group_names)
        self.tableWidget_selection.setHorizontalHeaderLabels(group_names)

        self.button_group = QtWidgets.QButtonGroup(self)
        for i, group1 in enumerate(self.cohort.groups):
            for j, group2 in enumerate(self.cohort.groups):
                if i == j:
                    item = QTableWidgetItem(" ")
                    item.setBackground(QtCore.Qt.lightGray)
                    item.setFlags(QtCore.Qt.NoItemFlags)
                    self.tableWidget_selection.setItem(i, j, item)
                else:
                    widget = QWidget()
                    layout = QHBoxLayout()
                    layout.setAlignment(QtCore.Qt.AlignHCenter)
                    radio_button = QRadioButton()
                    self.button_group.addButton(radio_button)
                    radio_button.group1 = group1
                    radio_button.group2 = group2
                    layout.addWidget(radio_button)
                    widget.setLayout(layout)
                    self.tableWidget_selection.setCellWidget(i, j, widget)
                    if group1 == selected_groups[0] and group2 == selected_groups[1]:
                        radio_button.setChecked(True)
        if not self.button_group.checkedButton():
            self.clear_comparison_table()
        self.button_group.buttonClicked.connect(self.comparison)

    def comparison(self):
        group_button = self.button_group.checkedButton()
        if group_button:
            if len(self.cohort.atlas.brain_regions) == 0:
                self.comparison_error("Atlas not loaded")
                return
            permutations = self.spinBoxPermutations.value()
            group_1 = group_button.group1
            group_2 = group_button.group2
            labels = ["Difference", "p-value (single-tailed)", "p-value (double-tailed)"]
            self.tableWidget_comparison.setRowCount(3)
            self.tableWidget_comparison.setVerticalHeaderLabels(labels)
            try:
                averages, stds, p_values = group_1.comparison(group_2, permutations=permutations)
                for i in range(len(averages[0])):
                    diff = averages[0][i] - averages[1][i]
                    item = QTableWidgetItem(str(diff))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_comparison.setItem(0, i, item)
                    item = QTableWidgetItem(str(p_values[0][i]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_comparison.setItem(1, i, item)
                    item = QTableWidgetItem(str(p_values[1][i]))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_comparison.setItem(2, i, item)
                self.btnExportTxt.setEnabled(True)
                return group_1, group_2, averages, stds, p_values
            except AssertionError as e:
                self.comparison_error(str(e))
                self.clear_comparison_table()
                self.btnExportTxt.setEnabled(False)

    def clear_comparison_table(self):
        self.tableWidget_comparison.clearContents()

    def export_as_txt(self):
        group_1, group_2, averages, stds, p_values = self.comparison()
        s = 'Comparison {} {}\n'.format(group_1.name, group_2.name)
        s += 'Average {} {}\n'.format(group_1.name, ' '.join(str(average) for average in averages[0]))
        s += 'Standard deviation {} {}\n'.format(group_1.name, ' '.join(str(std) for std in stds[0]))
        s += 'Average {} {}\n'.format(group_2.name, ' '.join(str(average) for average in averages[1]))
        s += 'Standard deviation {} {}\n'.format(group_2.name, ' '.join(str(std) for std in stds[1]))
        diff = averages[0] - averages[1]
        s += 'Difference {}\n'.format(' '.join(str(d) for d in diff))
        s += 'P-values single-tailed {}\n'.format(' '.join(str(value) for value in p_values[0]))
        s += 'P-values double-tailed {}\n'.format(' '.join(str(value) for value in p_values[1]))
        s += 'Permutations {}'.format(self.spinBoxPermutations.value())
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.saveFileName()", "comparison.txt", "text files (*.txt)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(s)

    def comparison_error(self, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle("Comparison error")
        msg_box.exec_()