from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.graph.measures.measure import Measure

ui_file = abs_path_from_relative(__file__, "../ui_files/measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_flags = (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def init(self, measure_type, analysis):
        self.analysis = analysis
        self.measure_type = measure_type
        if measure_type == Measure.GLOBAL:
            self.comboBoxRegion.hide()
        self.init_combo_boxes()
        self.btnMeasure.setChecked(True)
        self.measure()

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.tableWidget.selectAll)
        self.btnClearSelection.clicked.connect(self.tableWidget.clearSelection)
        self.btnRemove.clicked.connect(self.remove)

        self.btnMeasure.clicked.connect(self.measure)
        self.btnComparison.clicked.connect(self.comparison)
        self.btnRandomComparison.clicked.connect(self.random_comparison)

    def init_combo_boxes(self):
        self.comboBoxRegion.currentIndexChanged.connect(self.region_changed)
        self.comboBoxGroup1.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.group_changed)
        self.comboBoxRegion.currentIndexChanged.connect(self.update_table)

        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

        for label in self.analysis.cohort.atlas.get_brain_region_labels():
            self.comboBoxRegion.addItem(label)

    def remove(self):
        selected = self.get_selected()
        for i in range(len(selected) - 1, -1, -1):
            if self.btnMeasure.isChecked():
                index_to_remove = self.measurement_index_mapping[selected[i]]
                del self.analysis.measurements[index_to_remove]
            elif self.btnComparison.isChecked():
                index_to_remove = self.comparison_index_mapping[selected[i]]
                del self.analysis.comparisons[index_to_remove]
            elif self.btnRandomComparison.isChecked():
                index_to_remove = self.random_comparison_index_mapping[selected[i]]
                del self.analysis.random_comparisons[index_to_remove]
        self.update_table()

    def measure(self):
        self.comboBoxGroup2.setEnabled(False)
        self.update_table()

    def comparison(self):
        self.comboBoxGroup2.setEnabled(True)
        self.update_table()

    def random_comparison(self):
        self.comboBoxGroup2.setEnabled(False)
        self.update_table()

    def region_changed(self):
        self.update_table()

    def group_changed(self):
        self.update_table()

    def update_table(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        current_group_1 = self.comboBoxGroup1.currentIndex()
        current_group_2 = self.comboBoxGroup2.currentIndex()
        current_region_index = self.comboBoxRegion.currentIndex()
        if self.btnMeasure.isChecked():
            self.update_measurements_table(current_group_1, current_region_index)
        elif self.btnComparison.isChecked():
            self.update_comparison_table(current_group_1, current_group_2, current_region_index)
        elif self.btnRandomComparison.isChecked():
            self.update_random_comparison_table(current_group_1, current_region_index)

    def update_measurements_table(self, current_group, current_region_index):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['Value', 'Notes', 'Measure', 'Group', 'Param'])
        self.measurement_index_mapping = {}
        for i, measurement in enumerate(self.analysis.measurements):
            if measurement.dimension() == self.measure_type and current_group == measurement.group:
                row = self.tableWidget.rowCount()
                self.measurement_index_mapping[row] = i
                self.tableWidget.setRowCount(row + 1)
                contents = [(measurement.value), '-', measurement.sub_measure, self.analysis.cohort.groups[measurement.group].name, '-']
                for j, content in enumerate(contents):
                    if isinstance(content, np.ndarray):
                        content = content[current_region_index]
                    if not isinstance(content, str):
                        content = float_to_string(content)
                    item = QTableWidgetItem(content)
                    item.setFlags(self.table_flags)
                    self.tableWidget.setItem(row, j, item)

    def update_comparison_table(self, current_group_1, current_group_2, current_region_index):
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setHorizontalHeaderLabels(['Difference', 'p (1-tailed)', 'p (2-tailed)', 'Value 1', 'Value 2', 'CI lower', 'CI upper', 'Notes', 'Measure', 'Group 1', 'Group 2', 'Param'])
        self.comparison_index_mapping = {}
        for i, comparison in enumerate(self.analysis.comparisons):
            if comparison.dimension() == self.measure_type and current_group_1 == comparison.groups[0] and current_group_2 == comparison.groups[1]:
                row = self.tableWidget.rowCount()
                self.comparison_index_mapping[row] = i
                self.tableWidget.setRowCount(row + 1)
                contents = [(comparison.measures[1] - comparison.measures[0]), (comparison.p_values[0]),
                            (comparison.p_values[1]), (comparison.measures[0]),
                            (comparison.measures[1]), (comparison.confidence_interval[0]),
                            (comparison.confidence_interval[1]), '-',
                            comparison.sub_measure, self.analysis.cohort.groups[comparison.groups[0]].name,
                            self.analysis.cohort.groups[comparison.groups[1]].name, '-']
                for j, content in enumerate(contents):
                    if isinstance(content, np.ndarray):
                        content = content[current_region_index]
                    if not isinstance(content, str):
                        content = float_to_string(content)
                    item = QTableWidgetItem(content)
                    item.setFlags(self.table_flags)
                    self.tableWidget.setItem(row, j, item)

    def update_random_comparison_table(self, current_group, current_region_index):
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(['Comp value', 'p (1-tailed)', 'p (2-tailed)', 'Real value', 'CI lower', 'CI upper', 'Notes', 'Measure', 'Group', 'Param'])

    def get_selected(self):
        selected = [item.row() for item in self.tableWidget.selectionModel().selectedRows()]
        return selected

