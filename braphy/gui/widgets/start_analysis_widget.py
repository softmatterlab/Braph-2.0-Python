from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
import copy
from braphy.utility.helper_functions import abs_path_from_relative, FloatDelegate, float_to_string
from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI
from braphy.graph.measures.measure_parser import MeasureParser
from braphy.graph.measures.measure import Measure
from braphy.gui.community_structure_gui import CommunityStructure
from braphy.gui.calculate_group_measures import CalculateGroupMeasures
from braphy.gui.compare_group_measures import CompareGroupMeasures
from braphy.gui.compare_with_random_graph import CompareWithRandomGraph

ui_file = abs_path_from_relative(__file__, "../ui_files/start_analysis_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class StartAnalysisWidget(Base, Form):
    def __init__(self, parent = None):
        super(StartAnalysisWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, graph_analysis_gui):
        self.analysis_gui = graph_analysis_gui
        self.analysis = copy.deepcopy(self.analysis_gui.analysis)
        self.graph_type = self.analysis.graph_settings.graph_class()
        self.init_buttons()
        self.init_graph_measures_widget(self.graph_type)

    def init_buttons(self):
        self.btnViewCommunity.clicked.connect(self.view_community)
        self.btnNewAnalysis.clicked.connect(self.new_analysis)

        self.btnCalculate.clicked.connect(self.calculate_group_measures)
        self.btnCompare.clicked.connect(self.compare_group_measures)
        self.btnRandom.clicked.connect(self.compare_with_random_graph)

    def init_graph_measures_widget(self, graph_type):
        self.graphMeasuresWidget.init(graph_type)

    def view_community(self):
        self.community_structure = CommunityStructure(self.analysis_gui.analysis, self.analysis_gui.brain_mesh_data, self.analysis_gui.__class__)
        self.community_structure.set_locked(True)
        self.community_structure.show()

    def new_analysis(self):
        self.graph_analysis_gui = self.analysis_gui.__class__(subject_class = self.analysis_gui.subject_class,
                                                              analysis = self.analysis,
                                                              brain_mesh_data = self.analysis_gui.brain_mesh_data)
        self.graph_analysis_gui.show()

    def calculate_group_measures(self):
        self.calculate_group_measures_gui = CalculateGroupMeasures(self, self.analysis_gui.analysis, self.graph_type, self.table_update_callbacks())
        self.calculate_group_measures_gui.show()

    def compare_group_measures(self):
        self.compare_group_measures_gui = CompareGroupMeasures(self, self.analysis_gui.analysis, self.graph_type, self.table_update_callbacks())
        self.compare_group_measures_gui.show()

    def compare_with_random_graph(self):
        self.compare_with_random_graph_gui = CompareWithRandomGraph(self, self.analysis_gui.analysis, self.graph_type, self.table_update_callbacks())
        self.compare_with_random_graph_gui.show()

    def table_update_callbacks(self):
        return self.analysis_gui.table_update_callbacks()

    def show_buttons(self):
        for btn in [self.btnViewCommunity, self.btnNewAnalysis, self.btnCalculate, self.btnCompare, self.btnRandom]:
            btn.show()
        self.graphMeasuresWidget.show_buttons()

    def hide_buttons(self):
        for btn in [self.btnViewCommunity, self.btnNewAnalysis, self.btnCalculate, self.btnCompare, self.btnRandom]:
            btn.hide()
        self.graphMeasuresWidget.hide_buttons()
