from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem
from PyQt5.QtGui import QColor
from braphy.utility.helper_functions import abs_path_from_relative, QColor_to_list, QColor_from_list
import numpy as np

ui_file = abs_path_from_relative(__file__, "../ui_files/community_visualization_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class CommunityVisualizationWidget(Base, Form):
    def __init__(self, parent = None):
        super(CommunityVisualizationWidget, self).__init__(parent)
        self.setupUi(self)
        self.colors = []

    def init(self, community_structure, brain_region_change_callback):
        self.community_structure = community_structure
        self.brain_region_change_callback = brain_region_change_callback
        self.update_table()

    def update_table(self, community_structure = None):
        if community_structure is None:
            community_structure = self.community_structure
        self.community_structure = community_structure
        number_of_communities = max(community_structure)+1
        if number_of_communities < len(self.colors):
            self.colors = self.colors[:number_of_communities]
        self.tableWidget.setRowCount(number_of_communities)
        for i in range(number_of_communities):
            push_button = self.get_push_button_widget()
            self.tableWidget.setCellWidget(i, 0, push_button)
            if i >= len(self.colors):
                self.colors.append(QColor('blue'))
            color = self.colors[i]
            style_sheet = 'background-color: {};'.format(color.name())
            push_button.button.setStyleSheet(style_sheet)
            push_button.button.community = i
            self.update_brain_regions(i)

    def get_push_button_widget(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        push_button = QPushButton()
        push_button.clicked.connect(self.change_button_color)
        layout.addWidget(push_button)
        widget.setLayout(layout)
        widget.button = push_button
        return widget

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def change_button_color(self):
        color = self.pick_color()
        if color.isValid():
            style_sheet = 'background-color: {};'.format(color.name())
            btn = self.sender()
            btn.setStyleSheet(style_sheet)
            self.colors[btn.community] = color
            self.update_brain_regions(btn.community)

    def update_brain_regions(self, community):
        regions = np.where(np.array(self.community_structure) == community)[0]
        color = self.colors[community]
        self.brain_region_change_callback(color, regions)
