from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidgetItem
from PyQt5.QtGui import QColor
from braphy.utility.file_utility import abs_path_from_relative
from braphy.utility.qt_utility import QColor_to_list, QColor_from_list
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
        self.init_colors()
        self.group_index = group_index
        self.subject_index = 0
        self.brain_region_change_callback = brain_region_change_callback
        self.update_table(group_index)

    def init_colors(self):
        if len(self.community_structure[0].shape) < 2: #mri
            for group_index, array in self.community_structure.items():
                self.colors[group_index] = np.array([QColor('blue')]*array.shape[0])
        elif len(self.community_structure[0].shape) > 1: #fmri
            for group_index, array in self.community_structure.items():
                self.colors[group_index] = {}
                for subject_index in range(array.shape[0]):
                    self.colors[group_index][subject_index] = np.array([QColor('blue')]*array.shape[1])

    def update_table(self, group_index = None, subject_index = None):
        if isinstance(self.colors[self.group_index], np.ndarray):
            self.update_table_mri(group_index)
        else:
            self.update_table_fmri(group_index, subject_index)

    def update_table_mri(self, group_index = None):
        self.tableWidget.clear()
        if group_index is not None:
            self.group_index = group_index
        number_of_communities = self.number_of_communities_mri()
        if number_of_communities < len(self.colors[self.group_index]):
            self.colors[self.group_index] = self.colors[self.group_index][:number_of_communities]
        self.tableWidget.setRowCount(number_of_communities)
        self.tableWidget.setHorizontalHeaderLabels(['Community color'])
        for i in range(number_of_communities):
            push_button = self.get_push_button_widget()
            self.tableWidget.setCellWidget(i, 0, push_button)
            if i >= len(self.colors[self.group_index]):
                self.colors[self.group_index] = np.append(self.colors[self.group_index], [QColor('blue')])
            color = self.colors[self.group_index][i]
            style_sheet = 'background-color: {};'.format(color.name())
            push_button.button.setStyleSheet(style_sheet)
            push_button.button.community = i
            push_button.button.group_index = self.group_index
            push_button.button.subject_index = None
            self.update_brain_regions(i)

    def update_table_fmri(self, group_index, subject_index):
        self.tableWidget.clear()
        if group_index is not None:
            self.group_index = group_index
        if subject_index is not None:
            self.subject_index = subject_index
        number_of_communities = self.number_of_communities_fmri()
        if self.subject_index == -1:
            return
        if number_of_communities < len(self.colors[self.group_index][self.subject_index]):
            self.colors[self.group_index][self.subject_index] = self.colors[self.group_index][self.subject_index][:number_of_communities]
        self.tableWidget.setRowCount(number_of_communities)
        self.tableWidget.setHorizontalHeaderLabels(['Community color'])
        for i in range(number_of_communities):
            push_button = self.get_push_button_widget()
            self.tableWidget.setCellWidget(i, 0, push_button)
            if i >= len(self.colors[self.group_index][self.subject_index]):
                self.colors[self.group_index][self.subject_index] = np.append(self.colors[self.group_index][self.subject_index], [QColor('blue')])
            color = self.colors[self.group_index][self.subject_index][i]
            style_sheet = 'background-color: {};'.format(color.name())
            push_button.button.setStyleSheet(style_sheet)
            push_button.button.community = i
            push_button.button.group_index = self.group_index
            push_button.button.subject_index = self.subject_index
            self.update_brain_regions(i)

    def number_of_communities_mri(self):
        return int(np.max(self.community_structure[self.group_index])+1)

    def number_of_communities_fmri(self):
        return int(np.max(self.community_structure[self.group_index][self.subject_index,:])+1)

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
            if btn.subject_index is not None:
                self.colors[btn.group_index][btn.subject_index][btn.community] = color
            else:
                self.colors[btn.group_index][btn.community] = color
            self.update_brain_regions(btn.community)

    def update_brain_regions(self, community):
        if isinstance(self.colors[self.group_index], np.ndarray):
            regions = np.where(self.community_structure[self.group_index] == community)[0]
            color = self.colors[self.group_index][community]
        else:
            regions = np.where(self.community_structure[self.group_index][self.subject_index] == community)[0]
            color = self.colors[self.group_index][self.subject_index][community]
        self.brain_region_change_callback(color, regions)
