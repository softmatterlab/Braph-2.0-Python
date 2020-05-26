from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string

ui_file = abs_path_from_relative(__file__, "../ui_files/measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class MeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(MeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()

    def init(self, measure_type, analysis):
        self.analysis = analysis
        if measure_type == 'global':
            self.comboBoxRegion.hide()
            self.tableWidget.removeColumn(5)
        self.init_combo_boxes()
        self.btnMeasure.setChecked(True)
        self.measure()

    def init_buttons(self):
        self.btnSelectAll.clicked.connect(self.select_all)
        self.btnClearSelection.clicked.connect(self.clear_selection)
        self.btnRemove.clicked.connect(self.remove)

        self.btnMeasure.clicked.connect(self.measure)
        self.btnComparison.clicked.connect(self.comparison)
        self.btnRandomComparison.clicked.connect(self.random_comparison)

    def init_combo_boxes(self):
        self.comboBoxRegion.currentIndexChanged.connect(self.region_changed)
        self.comboBoxGroup1.currentIndexChanged.connect(self.group_changed)
        self.comboBoxGroup2.currentIndexChanged.connect(self.group_changed)

        for group in self.analysis.cohort.groups:
            self.comboBoxGroup1.addItem(group.name)
            self.comboBoxGroup2.addItem(group.name)

        for label in self.analysis.cohort.atlas.get_brain_region_labels():
            self.comboBoxRegion.addItem(label)

    def select_all(self):
        pass

    def clear_selection(self):
        pass

    def remove(self):
        pass

    def measure(self):
        print('measure')
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
        self.update_table()

    def group_changed(self):
        self.update_table()
        self.update_table()

    def update_table(self):
        pass

