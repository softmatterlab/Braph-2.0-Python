from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
import copy
from braphy.utility.file_utility import abs_path_from_relative
from braphy.utility.qt_utility import FloatDelegate
from braphy.utility.math_utility import float_to_string
from braphy.graph.measures.measure_parser import MeasureParser
from braphy.graph.measures.measure import Measure
from braphy.gui.community_structure_gui import CommunityStructure
from braphy.gui.calculate_group_measures import CalculateGroupMeasures
from braphy.gui.compare_group_measures import CompareGroupMeasures
from braphy.gui.compare_with_random_graph import CompareWithRandomGraph
from braphy.gui.calculation_window import CalculationWindow

ui_file = abs_path_from_relative(__file__, "../ui_files/start_analysis_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class StartAnalysisWidget(Base, Form):
    def __init__(self, parent = None):
        super(StartAnalysisWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, graph_analysis_gui):
        self.analysis_gui = graph_analysis_gui
        self.analysis = self.analysis_gui.analysis
        self.graph_type = self.analysis.graph_settings.graph_class()
        self.init_buttons()
        self.init_graph_measures_widget(self.graph_type)

    def init_buttons(self):
        self.btnViewCommunity.clicked.connect(self.view_community)
        self.btnNewAnalysis.clicked.connect(self.new_analysis)

        self.btnCalculate.clicked.connect(self.calculation_window)
        self.btnCompare.clicked.connect(self.calculation_window)
        self.btnRandom.clicked.connect(self.calculation_window)

    def init_graph_measures_widget(self, graph_type):
        self.graphMeasuresWidget.init(graph_type)

    def view_community(self):
        self.community_structure = CommunityStructure(self.analysis_gui.analysis, self.analysis_gui.brain_mesh_data, self.analysis_gui.__class__)
        self.community_structure.set_locked(True)
        self.community_structure.show()

    def new_analysis(self):
        self.graph_analysis_gui = self.analysis_gui.__class__(subject_class = self.analysis_gui.subject_class,
                                                              cohort = self.analysis.cohort,
                                                              brain_mesh_data = self.analysis_gui.brain_mesh_data)
        self.graph_analysis_gui.show()

    def calculation_window(self):
        self.calculation_window = CalculationWindow(self, self.analysis_gui.analysis, self.graph_type, self.update_callbacks())
        self.calculation_window.show()

    def calculate_group_measures(self):
        self.calculate_group_measures_gui = CalculateGroupMeasures(self, self.analysis_gui.analysis, self.graph_type, self.update_callbacks())
        self.calculate_group_measures_gui.show()

    def compare_group_measures(self):
        self.compare_group_measures_gui = CompareGroupMeasures(self, self.analysis_gui.analysis, self.graph_type, self.update_callbacks())
        self.compare_group_measures_gui.show()

    def compare_with_random_graph(self):
        self.compare_with_random_graph_gui = CompareWithRandomGraph(self, self.analysis_gui.analysis, self.graph_type, self.update_callbacks())
        self.compare_with_random_graph_gui.show()

    def update_callbacks(self):
        return self.analysis_gui.table_update_callbacks() + self.analysis_gui.visualization_update_callbacks()

    def show_buttons(self):
        for btn in [self.btnViewCommunity, self.btnNewAnalysis, self.btnCalculate, self.btnCompare, self.btnRandom]:
            btn.show()

    def hide_buttons(self):
        for btn in [self.btnViewCommunity, self.btnNewAnalysis, self.btnCalculate, self.btnCompare, self.btnRandom]:
            btn.hide()
        self.graphMeasuresWidget.hide_buttons()
