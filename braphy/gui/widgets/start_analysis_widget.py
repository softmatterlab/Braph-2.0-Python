from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.workflows import *
from braphy.graph.measures.measure_parser import MeasureParser

ui_file = abs_path_from_relative(__file__, "../ui_files/start_analysis_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class StartAnalysisWidget(Base, Form):
    def __init__(self, parent = None):
        super(StartAnalysisWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, graph_type):
        self.init_table(graph_type)

    def init_table(self, graph_type):
        descriptions = MeasureParser.list_measures_descriptions()
        measures_dict = MeasureParser.list_measures()

        measure_descriptions = {}
        for sub_measures in descriptions.values():
            for sub_measure, description in sub_measures.items():
                measure_descriptions[sub_measure] = description

        row = 0
        for measure_class, sub_measures in measures_dict[graph_type].items():
            for sub_measure in sub_measures:
                self.tableWidget.setRowCount(row + 1)
                item = QTableWidgetItem(sub_measure)
                item.setToolTip(measure_descriptions[sub_measure])
                self.tableWidget.setItem(row, 0, item)
                row += 1

