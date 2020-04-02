from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/graph_measures_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class GraphMeasuresWidget(Base, Form):
    def __init__(self, parent = None):
        super(GraphMeasuresWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self):
        pass
