import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QTableWidgetItem, QButtonGroup
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.widgets.brain_view_options_widget import BrainViewOptionsWidget
from braphy.workflows import *
import numpy as np

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/community_structure.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CommunityStructure(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, analysis, brain_mesh_data, AppWindow = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.analysis = analysis
        self.read_only = False
        self.brain_mesh_data = brain_mesh_data
        self.init_combo_box()
        self.init_buttons()
        self.init_table()
        self.init_brain_widget()
        self.init_actions()
        self.brain_view_options_widget.communityVisualizationWidget.init(self.analysis.community_structure, self.comboBoxGroup.currentIndex(), self.brainWidget.set_brain_region_color_list)
        if analysis.cohort.subject_class == SubjectMRI:
            self.btnGroup.hide()
            self.btnSubject.hide()
            self.comboBoxSubject.hide()

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxAlgorithm.addItem('Louvain')

    def init_buttons(self):
        self.btnFixed.toggled.connect(self.fixed_structure)
        self.btnDynamic.toggled.connect(self.dynamic_structure)

        self.btnSet.clicked.connect(self.set_community_structure)
        self.btnReset.clicked.connect(self.reset_community_structure)

        self.spinBoxGamma.setValue(self.analysis.get_gamma())
        self.spinBoxGamma.valueChanged.connect(self.set_gamma)

    def init_table(self):
        group_index = self.comboBoxGroup.currentIndex()
        self.update_table(self.analysis.community_structure[group_index])

    def init_actions(self):
        for action in self.brainWidget.get_actions():
            self.toolBar.addAction(action)
        for action in self.brain_view_options_widget.settingsWidget.get_actions():
            self.toolBar.addAction(action)
        self.actionGenerate_figure.triggered.connect(self.brainWidget.generate_figure)

    def init_brain_widget(self):
        self.brainWidget.init_brain_mesh(self.brain_mesh_data)
        color = self.palette().color(QtGui.QPalette.Window).getRgb()
        self.brainWidget.set_brain_background_color(color)

        self.brain_view_options_widget = BrainViewOptionsWidget(parent = self.groupBoxBrain)
        for i in [3,2,1]:
            self.brain_view_options_widget.tabWidget.removeTab(i)
        self.brain_view_options_widget.init(self.brainWidget)
        self.brain_view_options_widget.settingsWidget.change_transparency()
        self.brain_view_options_widget.show()

        show_only_selected = self.brain_view_options_widget.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.brain_view_options_widget.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.analysis.cohort.atlas.brain_regions, 4, [], show_brain_regions, show_only_selected)

        self.groupBoxBrain_old_resize = self.groupBoxBrain.resizeEvent
        self.groupBoxBrain.resizeEvent = self.resize_brain

    def set_gamma(self, gamma):
        self.analysis.set_gamma(gamma)
        self.update_table()

    def update_table(self, community_structure = None):
        if community_structure is None:
            community_structure = np.array(self.analysis.calculate_community_structure(self.comboBoxGroup.currentIndex()))
        self.community_structure = community_structure.copy()
        number_of_communities = self.number_of_communities()
        brain_regions = self.analysis.cohort.atlas.brain_regions
        self.tableWidget.setRowCount(len(brain_regions))
        self.tableWidget.setColumnCount(2 + number_of_communities)
        headers = ['Brain region']
        headers = headers + [str(community_number+1) for community_number in range(number_of_communities+2)]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i in range(len(brain_regions)):
            region = brain_regions[i]
            item = QTableWidgetItem(region.label)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, 0, item)
            button_group = QButtonGroup(self)
            for j in range(number_of_communities + 1):
                radio_button = self.get_radio_button_widget()
                if community_structure[i] == j:
                    radio_button.button.setChecked(True)
                if self.read_only:
                    radio_button.setDisabled(True)
                radio_button.button.region = i
                radio_button.button.community = j
                radio_button.button.clicked.connect(self.community_changed)
                button_group.addButton(radio_button.button)

                self.tableWidget.setCellWidget(i, 1 + j, radio_button)

    def number_of_communities(self):
        return int(np.max(self.community_structure) + 1)

    def get_radio_button_widget(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        radio_button = QRadioButton()
        layout.addWidget(radio_button)
        widget.setLayout(layout)
        widget.button = radio_button
        return widget

    def community_changed(self, checked):
        if not checked:
            return
        radio_button = self.sender()
        self.community_structure[radio_button.region] = radio_button.community
        self.minimize_community_indices()
        self.update_table(self.community_structure)

    def minimize_community_indices(self):
        for community in range(self.number_of_communities()):
            if community not in self.community_structure:
                for i in range(len(self.community_structure)):
                    if self.community_structure[i] > community:
                        self.community_structure[i] -= 1

    def fixed_structure(self, checked):
        if not checked:
            return
        disabled_items = [self.comboBoxAlgorithm, self.labelGamma, self.spinBoxGamma]
        for item in disabled_items:
            item.setDisabled(True)
        self.read_only = False
        self.update_table(self.community_structure)

    def dynamic_structure(self, checked):
        if not checked:
            return
        disabled_items = [self.comboBoxAlgorithm, self.labelGamma, self.spinBoxGamma]
        for item in disabled_items:
            item.setEnabled(True)
        self.read_only = True
        self.update_table()

    def group_changed(self, group_index):
        self.btnFixed.setChecked(True)
        community_structure = self.analysis.community_structure[group_index]
        self.update_table(community_structure)
        if self.brain_view_options_widget.community_tab_selected():
            self.brain_view_options_widget.communityVisualizationWidget.update_table(group_index)
        else:
            self.brain_view_options_widget.communityVisualizationWidget.group_index = group_index

    def set_community_structure(self):
        group_index = self.comboBoxGroup.currentIndex()
        self.analysis.community_structure[group_index,:] = self.community_structure.copy()
        self.brain_view_options_widget.communityVisualizationWidget.update_table(group_index)

    def reset_community_structure(self):
        group_index = self.comboBoxGroup.currentIndex()
        self.update_table(self.analysis.community_structure[group_index])

    def resize_brain(self, event):
        self.groupBoxBrain_old_resize(event)
        self.brain_view_options_widget.update_move()

    def resizeEvent(self, event):
        self.brain_view_options_widget.update_move()

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CommunityStructure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
