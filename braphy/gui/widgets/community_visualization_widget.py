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
        self.colors = {}

    def init(self, community_structure, group_index, brain_region_change_callback):
        self.community_structure = community_structure
        self.group_index = group_index
        self.brain_region_change_callback = brain_region_change_callback
        self.update_table()

    def update_table(self, group_index = 0):
        self.tableWidget.clear()
        self.group_index = group_index
        number_of_communities = self.number_of_communities()
        if group_index not in self.colors.keys():
            self.colors[group_index] = []
        if number_of_communities < len(self.colors[group_index]):
            self.colors[group_index] = self.colors[group_index][:number_of_communities]
        self.tableWidget.setRowCount(number_of_communities)
        for i in range(number_of_communities):
            push_button = self.get_push_button_widget()
            self.tableWidget.setCellWidget(i, 0, push_button)
            if i >= len(self.colors[group_index]):
                self.colors[group_index].append(QColor('blue'))
            color = self.colors[group_index][i]
            style_sheet = 'background-color: {};'.format(color.name())
            push_button.button.setStyleSheet(style_sheet)
            push_button.button.community = i
            push_button.button.group_index = group_index
            self.update_brain_regions(i)

    def number_of_communities(self):
        return int(np.max(self.community_structure[self.group_index])+1)

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
            self.colors[btn.group_index][btn.community] = color
            self.update_brain_regions(btn.community)

    def update_brain_regions(self, community):
        regions = np.where(self.community_structure[self.group_index] == community)[0]
        color = self.colors[self.group_index][community]
        self.brain_region_change_callback(color, regions)
