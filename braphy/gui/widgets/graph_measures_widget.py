from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.graph.measures.measure_parser import MeasureParser

ui_file = abs_path_from_relative(__file__, "../ui_files/graph_measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GraphMeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(GraphMeasuresWidget, self).__init__(parent)
        self.setupUi(self)
        size_policy = self.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)

        self.measures_dict = MeasureParser.list_measures()
        descriptions = MeasureParser.list_measures_descriptions()
        self.measures_dimensions = MeasureParser.list_measures_dimensions_str()
        self.measure_descriptions = {}
        for sub_measures in descriptions.values():
            for sub_measure, description in sub_measures.items():
                self.measure_descriptions[sub_measure] = description
        self.listWidgetMeasures.currentTextChanged.connect(self.update_description_text)

    def init(self, graph_type):
        self.update_measure_list(graph_type)

    def update_measure_list(self, graph_type):
        self.listWidgetMeasures.clear()
        for measure_class, sub_measures in self.measures_dict[graph_type].items():
            self.listWidgetMeasures.addItems(sub_measures)
        self.listWidgetMeasures.setCurrentRow(0)

    def update_description_text(self, text):
        if len(text) > 0:
            self.textBrowser.setText(self.measure_descriptions[text])
            self.textBrowserDimension.setText(self.measures_dimensions[text])
