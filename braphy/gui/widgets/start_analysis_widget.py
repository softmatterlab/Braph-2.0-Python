from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.workflows import *
from braphy.graph.measures.measure_parser import MeasureParser
from braphy.graph.measures.measure import Measure
from braphy.gui.community_structure_gui import CommunityStructure

ui_file = abs_path_from_relative(__file__, "../ui_files/start_analysis_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class StartAnalysisWidget(Base, Form):
    def __init__(self, parent = None):
        super(StartAnalysisWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, graph_type, graph_analysis_gui_class):
        self.init_table(graph_type)
        self.init_buttons(graph_analysis_gui_class)

    def init_table(self, graph_type):
        descriptions = MeasureParser.list_measures_descriptions()
        measures_dict = MeasureParser.list_measures()
        self.measures_dimensions = MeasureParser.list_measures_dimensions()

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
                item = QTableWidgetItem(Measure.dimensions_str(self.measures_dimensions[sub_measure]))
                self.tableWidget.setItem(row, 1, item)
                row += 1

    def init_buttons(self, graph_analysis_gui_class):
        self.btnSelectAll.clicked.connect(self.tableWidget.selectAll)
        self.btnClearSelection.clicked.connect(self.tableWidget.clearSelection)

        self.btnSelectGlobal.clicked.connect(lambda signal, dimension=Measure.GLOBAL: self.select_dimension(dimension))
        self.btnSelectNodal.clicked.connect(lambda signal, dimension=Measure.NODAL: self.select_dimension(dimension))
        self.btnSelectBinodal.clicked.connect(lambda signal, dimension=Measure.BINODAL: self.select_dimension(dimension))

        self.btnViewCommunity.clicked.connect(self.view_community)
        self.btnNewAnalysis.clicked.connect(lambda signal, cls=graph_analysis_gui_class: self.new_analysis(cls))

    def select_dimension(self, dimension):
        self.tableWidget.clearSelection()
        mode = self.tableWidget.selectionMode()
        self.tableWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        for row in range(self.tableWidget.rowCount()):
            sub_measure = self.tableWidget.item(row, 0).text()
            if self.measures_dimensions[sub_measure] == dimension:
                self.tableWidget.selectRow(row)
        self.tableWidget.setSelectionMode(mode)

    def view_community(self):
        self.community_structure = CommunityStructure()
        self.community_structure.show()

    def new_analysis(self, cls):
        self.graph_analysis_gui = cls()
        self.graph_analysis_gui.show()
