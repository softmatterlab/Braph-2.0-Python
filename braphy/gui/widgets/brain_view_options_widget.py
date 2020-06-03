from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_view_options_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BrainViewOptionsWidget(Base, Form):
    def __init__(self, parent = None):
        super(BrainViewOptionsWidget, self).__init__(parent)
        self.setupUi(self)

        self.icon_up = QtGui.QIcon()
        icon_location_up = abs_path_from_relative(__file__, "../icons/arrow_up.png")
        self.icon_up.addPixmap(QtGui.QPixmap(icon_location_up), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_down = QtGui.QIcon()
        icon_location_down = abs_path_from_relative(__file__, "../icons/arrow_down.png")
        self.icon_down.addPixmap(QtGui.QPixmap(icon_location_down), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnShow.setIcon(self.icon_up)

        self.setAutoFillBackground(True)
        self.tabWidget.hide()
        self.resize(self.sizeHint())
        self.btnShow.clicked.connect(self.update_visible)
        self.visible = False
        self.update_visible()
        self.tabWidget.currentChanged.connect(self.tab_changed)

    def init(self, brain_widget):
        self.brain_widget = brain_widget
        self.settingsWidget.init(brain_widget)
        self.groupVisualizationWidget.init(self.settingsWidget)
        self.subjectVisualizationWidget.init(self.settingsWidget)
        self.comparisonVisualizationWidget.init(self.settingsWidget)

        self.add_custom_colormap_callbacks()

    def add_custom_colormap_callbacks(self):
        callback_subject = self.subjectVisualizationWidget.comboBoxColormap.add_colormap
        callback_group = self.groupVisualizationWidget.comboBoxColormap.add_colormap
        callback_comparison = self.comparisonVisualizationWidget.comboBoxColormap.add_colormap

        self.subjectVisualizationWidget.comboBoxColormap.set_custom_color_map_callbacks([callback_group, callback_comparison])
        self.groupVisualizationWidget.comboBoxColormap.set_custom_color_map_callbacks([callback_subject, callback_comparison])
        self.comparisonVisualizationWidget.comboBoxColormap.set_custom_color_map_callbacks([callback_subject, callback_group])

    def set_groups(self, groups):
        self.groupVisualizationWidget.set_list(groups)
        self.comparisonVisualizationWidget.set_list(groups)

    def set_subjects(self, subjects):
        self.subjectVisualizationWidget.set_list(subjects)

    def tab_changed(self, index):
        if index == self.tabWidget.indexOf(self.tabPlot):
            self.brain_widget.reset_brain_region_colors()
            self.settingsWidget.change_brain_region_size()
            self.brain_widget.enable_brain_region_selection(True)

        elif index == self.tabWidget.indexOf(self.tabSubjects):
            self.subjectVisualizationWidget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)

        elif index == self.tabWidget.indexOf(self.tabGroups):
            self.groupVisualizationWidget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)

        elif index == self.tabWidget.indexOf(self.tabComparison):
            self.comparisonVisualizationWidget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)

        elif index == self.tabWidget.indexOf(self.tabCommunity):
            self.communityVisualizationWidget.update_table()
            self.brain_widget.enable_brain_region_selection(False)

    def community_tab_selected(self):
        return self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabCommunity)

    def update_move(self):
        self.move(9, self.parent().height()-self.height() - 9)

    def update_visible(self):
        if self.visible:
            self.tabWidget.show()
            self.btnShow.setIcon(self.icon_down)
            self.resize(self.sizeHint())
            self.visible = False
        else:
            self.tabWidget.hide()
            self.btnShow.setIcon(self.icon_up)
            self.resize(100, 20)
            self.visible = True
        self.update_move()


