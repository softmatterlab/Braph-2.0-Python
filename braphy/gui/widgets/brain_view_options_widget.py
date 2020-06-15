from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from pyqtgraph import ColorMap as cm
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.widgets.graph_view_widget import GraphViewWidget
from braphy.gui.widgets.visualization_widget import *
from braphy.gui.widgets.community_visualization_widget import CommunityVisualizationWidget
from braphy.gui.widgets.measure_visualization_widget import MeasureVisualizationWidget
from braphy.gui.widgets.measure_comparison_visualization_widget import MeasureComparisonVisualizationWidget

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

        self.graph_view_widget = GraphViewWidget()
        self.subject_visualization_widget = SubjectVisualizationWidget()
        self.group_visualization_widget = GroupVisualizationWidget()
        self.comparison_visualization_widget = ComparisonVisualizationWidget()
        self.community_visualization_widget = CommunityVisualizationWidget()
        self.measure_visualization_widget = MeasureVisualizationWidget()
        self.measure_comparison_visualization_widget = MeasureComparisonVisualizationWidget()

    def init(self, brain_widget):
        self.brain_widget = brain_widget
        self.settingsWidget.init(brain_widget)

    def add_graph_view_tab(self, analysis):
        self.graph_view_widget.init(self.brain_widget, analysis)
        self.tabWidget.addTab(self.graph_view_widget, 'View graph')

    def add_visualize_measure_tab(self, measurements, groups):
        self.measure_visualization_widget.init(self.settingsWidget, measurements, groups)
        self.tabWidget.addTab(self.measure_visualization_widget, 'Visualize measures')

    def add_visualize_measure_comparison_tab(self, comparisons, groups):
        self.measure_comparison_visualization_widget.init(self.settingsWidget, comparisons, groups)
        self.tabWidget.addTab(self.measure_comparison_visualization_widget, 'Visualize comparisons')

    def add_visualize_subjects_tab(self):
        self.subject_visualization_widget.init(self.settingsWidget)
        self.tabWidget.addTab(self.subject_visualization_widget, 'Visualize subjects')

    def add_visualize_groups_tab(self):
        self.group_visualization_widget.init(self.settingsWidget)
        self.tabWidget.addTab(self.group_visualization_widget, 'Visualize groups')

    def add_visualize_comparison_tab(self):
        self.comparison_visualization_widget.init(self.settingsWidget)
        self.tabWidget.addTab(self.comparison_visualization_widget, 'Visualize comparison')

    def add_visualize_communities_tab(self, community_structure, group_index, color_callback):
        self.community_visualization_widget.init(community_structure, group_index, color_callback)
        self.tabWidget.addTab(self.community_visualization_widget, 'Visualize communities')

    def set_cohort_mode(self):
        self.add_visualize_subjects_tab()
        self.add_visualize_groups_tab()
        self.add_visualize_comparison_tab()
        self.add_custom_colormap_callbacks()

    def set_graph_analysis_mode(self, analysis):
        self.add_graph_view_tab(analysis)
        self.add_visualize_measure_tab(analysis.measurements, analysis.cohort.groups)
        self.add_visualize_measure_comparison_tab(analysis.comparisons, analysis.cohort.groups)

    def add_custom_colormap_callbacks(self):
        callback_subject = self.subject_visualization_widget.comboBoxColormap.add_colormap
        callback_group = self.group_visualization_widget.comboBoxColormap.add_colormap
        callback_comparison = self.comparison_visualization_widget.comboBoxColormap.add_colormap

        self.subject_visualization_widget.comboBoxColormap.set_custom_color_map_callbacks([callback_group, callback_comparison])
        self.group_visualization_widget.comboBoxColormap.set_custom_color_map_callbacks([callback_subject, callback_comparison])
        self.comparison_visualization_widget.comboBoxColormap.set_custom_color_map_callbacks([callback_subject, callback_group])

    def set_groups(self, groups):
        self.group_visualization_widget.set_list(groups)
        self.comparison_visualization_widget.set_list(groups)

    def set_subjects(self, subjects):
        self.subject_visualization_widget.set_list(subjects)

    def tab_changed(self, index):
        if index == self.tabWidget.indexOf(self.tabPlot):
            self.brain_widget.reset_brain_region_colors()
            self.settingsWidget.change_brain_region_size()
            self.brain_widget.enable_brain_region_selection(True)
            self.brain_widget.clear_gui_brain_edges()
        elif index == self.tabWidget.indexOf(self.subject_visualization_widget):
            self.subject_visualization_widget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)
        elif index == self.tabWidget.indexOf(self.group_visualization_widget):
            self.group_visualization_widget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)
        elif index == self.tabWidget.indexOf(self.comparison_visualization_widget):
            self.comparison_visualization_widget.update_visualization()
            self.brain_widget.enable_brain_region_selection(False)
        elif index == self.tabWidget.indexOf(self.community_visualization_widget):
            self.community_visualization_widget.update_table()
            self.brain_widget.enable_brain_region_selection(False)
        elif index == self.tabWidget.indexOf(self.measure_visualization_widget):
            self.brain_widget.clear_gui_brain_edges()
            self.measure_visualization_widget.update_visualization()
        elif index == self.tabWidget.indexOf(self.graph_view_widget):
            self.graph_view_widget.update_visualization()

    def community_tab_selected(self):
        return self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.community_visualization_widget)

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


