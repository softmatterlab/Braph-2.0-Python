import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QTableWidgetItem, QButtonGroup, QAbstractItemView
from braphy.utility.helper_functions import abs_path_from_relative
from braphy.gui.widgets.brain_view_options_widget import BrainViewOptionsWidget
from braphy.workflows.MRI.subject_MRI import SubjectMRI
from braphy.workflows.fMRI.subject_fMRI import SubjectfMRI
import numpy as np

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/community_structure.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CommunityStructure(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, analysis, brain_mesh_data, start_analysis_gui_function, AppWindow = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.analysis = analysis
        self.read_only = False
        self.locked = False
        self.brain_mesh_data = brain_mesh_data
        self.start_analysis_gui_function = start_analysis_gui_function
        self.init_combo_box()
        self.init_buttons()
        self.init_brain_widget()
        self.init_actions()
        self.brain_view_options_widget.add_visualize_communities_tab(self.analysis.community_structure, self.comboBoxGroup.currentIndex(), self.brainWidget.set_brain_region_color_list)
        self.group_changed(0)
        self.init_community_structure()
        if analysis.cohort.subject_class == SubjectMRI:
            self.btnGroup.hide()
            self.btnSubject.hide()
            self.comboBoxSubject.hide()
        elif analysis.cohort.subject_class == SubjectfMRI:
            self.btnSubject.setChecked(True)
        if analysis.graph_settings.weighted:
            self.labelBinary.hide()
            self.spinBoxBinary.hide()
        else:
            self.labelBinary.setText(analysis.graph_settings.rule_binary)
        self.fixed_structure(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBoxGroup.addItem(group.name)
        self.comboBoxGroup.currentIndexChanged.connect(self.group_changed)
        self.comboBoxSubject.currentIndexChanged.connect(self.subject_changed)
        self.comboBoxAlgorithm.addItem('Louvain')

    def init_buttons(self):
        self.btnGroup.toggled.connect(self.group_average)
        self.btnSubject.toggled.connect(self.subject)

        self.btnFixed.toggled.connect(self.fixed_structure)
        self.btnDynamic.toggled.connect(self.dynamic_structure)

        self.btnSet.clicked.connect(self.set_community_structure)
        self.btnSetAll.clicked.connect(self.set_all_community_structure)
        self.btnReset.clicked.connect(self.reset_community_structure)
        self.btnSubgraphAnalysis.clicked.connect(self.start_subgraph_analysis)

        self.spinBoxGamma.setValue(self.analysis.get_gamma())
        self.spinBoxGamma.valueChanged.connect(self.set_gamma)
        self.spinBoxBinary.setValue(self.analysis.get_binary_value())
        self.spinBoxBinary.valueChanged.connect(self.set_binary_value)

    def init_community_structure(self):
        self.community_structure = self.get_community_structure()
        self.update_table(self.community_structure)

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

        self.brain_view_options_widget.init(self.brainWidget)
        self.brain_view_options_widget.settingsWidget.change_transparency()
        self.brain_view_options_widget.show()

        show_only_selected = self.brain_view_options_widget.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.brain_view_options_widget.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.analysis.cohort.atlas.brain_regions, 4, [], show_brain_regions, show_only_selected)

        self.groupBoxBrain_old_resize = self.groupBoxBrain.resizeEvent
        self.groupBoxBrain.resizeEvent = self.resize_brain

    def set_locked(self, locked):
        self.locked = locked
        items = [self.btnGroup, self.btnSubject, self.comboBoxSubject, self.btnFixed,
                 self.btnDynamic, self.comboBoxAlgorithm, self.labelGamma, self.spinBoxGamma,
                 self.labelBinary, self.spinBoxBinary, self.btnSet, self.btnSetAll, self.btnReset]
        for item in items:
            item.setEnabled(not locked)
        self.init_community_structure()

    def set_gamma(self, gamma):
        self.analysis.set_gamma(gamma)
        self.update_table()

    def set_binary_value(self, value):
        self.analysis.set_binary_value(value)
        self.update_table()

    def update_table(self, community_structure = None):
        if community_structure is None:
            self.community_structure = self.calculate_community_structure()
        else:
            self.community_structure = community_structure

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
                if self.community_structure[i] == j:
                    radio_button.button.setChecked(True)
                if self.read_only or self.locked:
                    radio_button.setDisabled(True)
                radio_button.button.region = i
                radio_button.button.community = j
                radio_button.button.clicked.connect(self.community_changed)
                button_group.addButton(radio_button.button)

                self.tableWidget.setCellWidget(i, 1 + j, radio_button)

    def calculate_community_structure(self):
        group_index = self.comboBoxGroup.currentIndex()
        if self.analysis.is_MRI():
            community_structure = np.array(self.analysis.calculate_community_structure(group_index))
        elif self.analysis.is_fMRI():
            if self.btnGroup.isChecked():
                community_structure = np.array(self.analysis.calculate_community_structure(group_index))
            else:
                subject_index = self.comboBoxSubject.currentIndex()
                community_structure = np.array(self.analysis.calculate_community_structure(group_index, subject_index))
        return community_structure

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
        group_index = self.comboBoxGroup.currentIndex()
        subject_index = self.comboBoxSubject.currentIndex()
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

    def group_average(self, checked):
        if not checked:
            return
        self.btnReset.setEnabled(False)
        self.btnSet.setText('Set for current group')
        self.btnDynamic.setChecked(True)
        self.comboBoxSubject.blockSignals(True)
        self.comboBoxSubject.setEnabled(False)
        self.comboBoxSubject.clear()
        self.comboBoxSubject.blockSignals(False)
        self.update_table()

    def subject(self, checked):
        if not checked:
            return
        self.btnReset.setEnabled(True)
        self.btnSet.setText('Set for current subject')
        self.comboBoxSubject.setEnabled(True)
        self.update_subjects()
        self.btnFixed.setChecked(True)
        self.update_table(self.get_community_structure())

    def update_subjects(self):
        group_index = self.comboBoxGroup.currentIndex()
        self.comboBoxSubject.blockSignals(True)
        self.comboBoxSubject.clear()
        for subject in self.analysis.cohort.groups[group_index].subjects:
            self.comboBoxSubject.addItem(subject.id)
        self.comboBoxSubject.blockSignals(False)

    def fixed_structure(self, checked):
        if not checked:
            return
        self.lock_structure_settings(True)
        self.read_only = False
        self.update_table(self.community_structure)

    def dynamic_structure(self, checked):
        if not checked:
            return
        self.lock_structure_settings(False)
        self.read_only = True
        self.update_table()

    def lock_structure_settings(self, locked):
        items = [self.comboBoxAlgorithm, self.labelGamma, self.spinBoxGamma,
                 self.labelBinary, self.spinBoxBinary]
        for item in items:
            item.setDisabled(locked)

    def group_changed(self, group_index):
        self.btnFixed.setChecked(True)
        if self.analysis.is_fMRI():
            self.update_subjects()
        if self.brain_view_options_widget.community_tab_selected():
            if self.analysis.is_fMRI():
                self.brain_view_options_widget.community_visualization_widget.update_table(group_index, 0)
            else:
                self.brain_view_options_widget.community_visualization_widget.update_table(group_index)
        else:
            self.brain_view_options_widget.community_visualization_widget.group_index = group_index
            self.brain_view_options_widget.community_visualization_widget.subject_index = 0
        community_structure = self.get_community_structure()
        self.update_table(community_structure)

    def get_community_structure(self): # get saved community for current group (and subject)
        community_structure = self.analysis.community_structure
        group_index = self.comboBoxGroup.currentIndex()
        subject_index = self.comboBoxSubject.currentIndex()
        if subject_index == -1:
            community_structure = community_structure[group_index]
        else:
            community_structure = community_structure[group_index][subject_index, :]
        return community_structure.copy()

    def subject_changed(self, subject_index):
        self.btnFixed.setChecked(True)
        group_index = self.comboBoxGroup.currentIndex()
        if self.brain_view_options_widget.community_tab_selected():
            if self.analysis.is_fMRI():
                self.brain_view_options_widget.community_visualization_widget.update_table(group_index, subject_index)
            else:
                self.brain_view_options_widget.community_visualization_widget.update_table(group_index)
        else:
            self.brain_view_options_widget.community_visualization_widget.group_index = group_index
            self.brain_view_options_widget.community_visualization_widget.subject_index = subject_index
        self.update_table(self.get_community_structure())

    def set_community_structure(self):
        group_index = self.comboBoxGroup.currentIndex()
        subject_index = self.comboBoxSubject.currentIndex()
        if subject_index != -1: #fmri subject
            self.analysis.set_community_structure(group_index, self.community_structure.copy(), subject_index)
            self.brain_view_options_widget.community_visualization_widget.update_table(group_index, subject_index)
        else: #mri or fmri group average
            self.analysis.set_community_structure(group_index, self.community_structure.copy())
            if not self.btnGroup.isChecked():
                self.brain_view_options_widget.community_visualization_widget.update_table(group_index)

    def set_all_community_structure(self):
        for i, group in enumerate(self.analysis.cohort.groups):
            self.analysis.set_community_structure(i, self.community_structure.copy())
        group_index = self.comboBoxGroup.currentIndex()
        subject_index = self.comboBoxSubject.currentIndex()
        if self.analysis.is_MRI():
            self.brain_view_options_widget.community_visualization_widget.update_table(group_index)
        else:
            self.brain_view_options_widget.community_visualization_widget.update_table(group_index, subject_index)

    def reset_community_structure(self):
        self.btnFixed.setChecked(True)
        community_structure = self.get_community_structure()
        self.update_table(community_structure)

    def start_subgraph_analysis(self):
        columns = [item.column() for item in self.tableWidget.selectionModel().selectedColumns()]
        if not columns:
            return
        column = columns[0]
        selected_nodes = []
        for row in range(self.tableWidget.rowCount()):
            widget = self.tableWidget.cellWidget(row, column)
            button = widget.button
            if button.isChecked():
                selected_nodes.append(row)
        if not selected_nodes:
            return
        subgraph_analysis = self.analysis.get_subgraph_analysis(selected_nodes)
        self.subgraph_analysis_gui = self.start_analysis_gui_function(analysis = subgraph_analysis,
                                                                      brain_mesh_data = self.brain_mesh_data)
        self.subgraph_analysis_gui.show()

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
