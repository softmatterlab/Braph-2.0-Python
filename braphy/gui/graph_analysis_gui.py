import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.graph.graphs import *
from braphy.graph.measures.measure import Measure
from braphy.graph.measures.measure_parser import MeasureParser
from braphy.graph.graph_factory import GraphSettings
from braphy.cohort.cohort import Cohort
from braphy.gui.cohort_editor_gui import CohortEditor
from braphy.analysis.analysis import Analysis
from braphy.gui.community_structure_gui import CommunityStructure
from braphy.gui.widgets.brain_view_options_widget import BrainViewOptionsWidget
from braphy.utility.helper_functions import abs_path_from_relative, same_class, get_analysis_class
from braphy.gui.exit_dialog import ExitDialog

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/graph_analysis.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class GraphAnalysis(ExitDialog, Ui_MainWindow):
    def __init__(self, subject_class, AppWindow = None, cohort = None, analysis = None, brain_mesh_data = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)

        self.init_buttons()
        self.init_actions()
        self.init_comboboxes()
        self.startAnalysisWidget.init_graph_measures_widget(self.get_graph_settings().graph_class())
        self.startAnalysisWidget.hide_buttons()
        self.tabWidget.tabBar().hide()
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.brain_view_options_widget = BrainViewOptionsWidget(parent=self.tabBrainView)
        self.brain_view_options_widget.raise_()

        if analysis:
            self.subject_class = analysis.cohort.subject_class
            if brain_mesh_data:
                self.brain_mesh_data = brain_mesh_data
            self.analysis_class = analysis.__class__
        else:
            self.analysis = None
            self.subject_class = subject_class
            self.analysis_class = get_analysis_class('Analysis{}'.format(self.subject_class.data_type()))
        if self.subject_class.structural():
            self.correlationMatrixWidget.set_structural_view()
            self.repetitionLabel.hide()
        self.setWindowTitle('{} Graph Analysis'.format(self.subject_class.data_type()))

        self.btnViewCohort.setEnabled(False)
        self.file_name = None
        self.textAnalysisName.textChanged.connect(self.set_analysis_name)
        self.set_locked(True)

        if analysis:
            self.analysis = analysis
            self.init_analysis()
        if cohort:
            assert same_class(cohort.subject_class, self.subject_class), \
                   'Cohort subject class {} does not match graph analysis subject class: {}'.format(cohort.subject_class, self.subject_class)
            self.set_cohort(cohort)
        if brain_mesh_data:
            self.brain_mesh_data = brain_mesh_data

    def to_dict(self):
        d = {}
        if self.analysis is not None:
            d['analysis'] = self.analysis.to_dict()
        brain_mesh_data = {}
        brain_mesh_data['vertices'] = self.brain_mesh_data['vertices'].tolist()
        brain_mesh_data['faces'] = self.brain_mesh_data['faces'].tolist()
        d['brain_mesh_data'] = brain_mesh_data
        return d

    def to_file(self, file_name):
        self.file_name = file_name
        with open(file_name, 'w') as f:
            json.dump(self.to_dict(), f, sort_keys=True, indent=4)

    def from_dict(self, d):
        self.analysis = self.analysis_class.from_dict(d['analysis'])
        self.init_brain_mesh(d)
        self.init_analysis()

    def from_file(self, file_name):
        with open(file_name, 'r') as f:
            d = json.load(f)
        self.from_dict(d)
        self.set_locked(False)
        self.file_name = file_name

    def init_brain_mesh(self, d):
        vertices = np.asarray(d['brain_mesh_data']['vertices'])
        faces = np.asarray(d['brain_mesh_data']['faces'])
        brain_mesh_data = {'vertices': vertices, 'faces': faces}
        self.brain_mesh_data = brain_mesh_data

    def init_brain_widget(self):
        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        self.brain_view_options_widget.init(self.brainWidget)
        self.brain_view_options_widget.settingsWidget.change_transparency()
        self.brain_view_options_widget.set_graph_analysis_mode(self.analysis)
        self.brain_view_options_widget.show()

    def set_locked(self, locked):
        lock_items = [self.correlationMatrixWidget, self.textAnalysisName, self.comboBoxWeighted, self.comboBoxDirected,
                      self.comboBoxCorrelation, self.comboBoxNegative, self.comboBoxBinary,
                      self.btnStartAnalysis, self.groupBoxCommunityStructure, self.startAnalysisWidget,
                      self.comboBoxSymmetrize, self.comboBoxStandardize, self.actionSave, self.actionSave_as]
        for item in lock_items:
            item.setEnabled(not locked)

    def init_buttons(self):
        self.btnSelectCohort.clicked.connect(self.select_cohort)
        self.btnViewCohort.clicked.connect(self.view_cohort)
        self.btnEdit.clicked.connect(self.edit_community)
        self.btnDefault.clicked.connect(self.default)
        self.btnStartAnalysis.clicked.connect(self.start_analysis)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)
        self.actionImport_xml.triggered.connect(self.import_xml)
        self.actionExport_xml.triggered.connect(self.export_xml)
        self.actionQuit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

    def init_brain_view_actions(self):
        for action in self.brainWidget.get_actions():
            self.toolBar.addAction(action)
        for action in self.brain_view_options_widget.settingsWidget.get_actions():
            self.toolBar.addAction(action)
        self.set_brain_view_actions_visible(False)

    def set_brain_view_actions_visible(self, state):
        for action in self.brainWidget.get_actions():
            action.setVisible(state)
        for action in self.brain_view_options_widget.settingsWidget.get_actions():
            action.setVisible(state)

    def init_correlation_matrix_actions(self):
        for action in self.correlationMatrixWidget.get_actions():
            self.toolBar.addAction(action)

    def set_correlation_actions_visible(self, state):
        for action in self.correlationMatrixWidget.get_actions():
            action.setVisible(state)

    def init_binary_plot_actions(self):
        for action in self.globalMeasuresWidget.binaryPlotWidget.get_actions():
            self.toolBar.addAction(action)
        for action in self.nodalMeasuresWidget.binaryPlotWidget.get_actions():
            self.toolBar.addAction(action)
        for action in self.binodalMeasuresWidget.binaryPlotWidget.get_actions():
            self.toolBar.addAction(action)
        self.set_binary_plot_actions_visible([self.globalMeasuresWidget, self.nodalMeasuresWidget, self.binodalMeasuresWidget], False)

    def set_binary_plot_actions_visible(self, widgets, state):
        if self.analysis.graph_settings.weighted and state:
            return
        for widget in widgets:
            for action in widget.binaryPlotWidget.get_actions():
                action.setVisible(state)

    def init_comboboxes(self):
        correlations = ['pearson', 'spearman', 'kendall', 'partial pearson', 'partial spearman']
        negative = ['zero', 'none', 'abs']
        binary = ['threshold', 'density']
        symmetrize = ['sum', 'average', 'min', 'max']
        standardize = ['range', 'threshold']
        self.comboBoxWeighted.addItems(['True', 'False'])
        self.comboBoxDirected.addItems(['True', 'False'])
        self.comboBoxCorrelation.addItems(correlations)
        self.comboBoxNegative.addItems(negative)
        self.comboBoxBinary.addItems(binary)
        self.comboBoxSymmetrize.addItems(symmetrize)
        self.comboBoxStandardize.addItems(standardize)

        self.comboBoxWeighted.currentTextChanged.connect(lambda signal: self.set_weighted(eval(signal)))
        self.comboBoxDirected.currentTextChanged.connect(lambda signal: self.set_directed(eval(signal)))
        self.comboBoxCorrelation.currentTextChanged.connect(self.set_correlation)
        self.comboBoxNegative.currentTextChanged.connect(self.set_negative_rule)
        self.comboBoxBinary.currentTextChanged.connect(self.set_binary_rule)
        self.comboBoxSymmetrize.currentTextChanged.connect(self.set_symmetrize_rule)
        self.comboBoxStandardize.currentTextChanged.connect(self.set_standardize_rule)

    def tab_changed(self):
        if self.tabWidget.currentIndex() == 0:
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(True)
            self.set_binary_plot_actions_visible([self.globalMeasuresWidget, self.nodalMeasuresWidget, self.binodalMeasuresWidget], False)
        elif self.tabWidget.currentIndex() == 1:
            self.globalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
            self.set_binary_plot_actions_visible([self.nodalMeasuresWidget, self.binodalMeasuresWidget], False)
            self.set_binary_plot_actions_visible([self.globalMeasuresWidget], True)
        elif self.tabWidget.currentIndex() == 2:
            self.nodalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
            self.set_binary_plot_actions_visible([self.globalMeasuresWidget, self.binodalMeasuresWidget], False)
            self.set_binary_plot_actions_visible([self.nodalMeasuresWidget], True)
        elif self.tabWidget.currentIndex() == 3:
            self.binodalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
            self.set_binary_plot_actions_visible([self.globalMeasuresWidget, self.nodalMeasuresWidget], False)
            self.set_binary_plot_actions_visible([self.binodalMeasuresWidget], True)
        elif self.tabWidget.currentIndex() == 4:
            self.set_brain_view_actions_visible(True)
            self.set_correlation_actions_visible(False)
            self.set_binary_plot_actions_visible([self.globalMeasuresWidget, self.nodalMeasuresWidget, self.binodalMeasuresWidget], False)
            self.brain_view_options_widget.update_move()

    def set_analysis_name(self, name):
        if self.analysis:
            self.analysis.set_name(name)

    def select_cohort(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self,"Load cohort", "",
                                                   "cohort files (*.cohort)", options = options)
        if file_name:
            with open(file_name, 'r') as f:
                cohort_dict = json.load(f)
                cohort = Cohort.from_dict(cohort_dict['cohort'])
                vertices = np.asarray(cohort_dict['brain_mesh_data']['vertices'])
                faces = np.asarray(cohort_dict['brain_mesh_data']['faces'])
                brain_mesh_data = {'vertices': vertices, 'faces': faces}
                self.brain_mesh_data = brain_mesh_data
                if not same_class(cohort.subject_class, self.subject_class):
                    self.import_error('Wrong data type. Load a cohort with subjects of type {} instead.'.format(self.subject_class.__name__))
                    return
                if len(cohort.groups) == 0 or len(cohort.subjects) == 0:
                    self.import_error('Can only perform an analysis on a cohort with groups and subjects.')
                    return
                self.set_cohort(cohort)

    def set_cohort(self, cohort):
        graph_settings = self.get_graph_settings()
        analysis = self.analysis_class(cohort, graph_settings)
        self.analysis = analysis
        self.init_analysis()
        self.set_graph_type()

    def init_analysis(self):
        self.textAnalysisName.setText(self.analysis.name)
        self.btnViewCohort.setEnabled(True)
        self.set_locked(False)
        self.set_weighted(eval(self.comboBoxWeighted.currentText()))
        self.set_directed(eval(self.comboBoxDirected.currentText()))
        self.correlationMatrixWidget.init(self.analysis)
        self.set_cohort_labels()
        self.init_correlation_matrix_actions()
        self.init_binary_plot_actions()
        self.init_brain_view_actions()
        self.update_community_number()

    def get_graph_settings(self):
        weighted = eval(self.comboBoxWeighted.currentText())
        directed = eval(self.comboBoxDirected.currentText())
        gamma = 1
        community_algorithm = 'Louvain'
        rule_negative = self.comboBoxNegative.currentText()
        rule_symmetrize = self.comboBoxSymmetrize.currentText()
        rule_standardize = self.comboBoxStandardize.currentText()
        rule_binary = self.comboBoxBinary.currentText()
        value_binary = 0
        rule_correlation = self.comboBoxCorrelation.currentText()
        graph_settings = GraphSettings(weighted, directed, gamma, community_algorithm,
                                        rule_negative, rule_symmetrize, rule_standardize, rule_binary,
                                        value_binary, rule_correlation)
        return graph_settings

    def set_cohort_labels(self):
        self.subjectLabel.setText('Number of subjects = {}'.format(len(self.analysis.cohort.subjects)))
        self.groupLabel.setText('Number of groups = {}'.format(len(self.analysis.cohort.groups)))

    def view_cohort(self):
        self.cohort_editor_gui = CohortEditor(self.subject_class, self, self.analysis.cohort, brain_mesh_data = self.brain_mesh_data)
        self.cohort_editor_gui.set_read_only()
        self.cohort_editor_gui.show()

    def edit_community(self):
        self.community_structure_gui = CommunityStructure(self.analysis, self.brain_mesh_data, self.__class__, AppWindow = self)
        self.community_structure_gui.show()

    def default(self):
        self.analysis.set_default_community_structure()

    def start_analysis(self):
        self.groupBoxCommunityStructure.hide()
        self.startAnalysisWidget.show_buttons()
        self.btnStartAnalysis.hide()

        self.comboBoxCorrelation.setEnabled(False)
        self.comboBoxWeighted.setEnabled(False)
        self.comboBoxDirected.setEnabled(False)
        self.comboBoxNegative.setEnabled(False)
        self.comboBoxBinary.setEnabled(False)
        self.comboBoxSymmetrize.setEnabled(False)
        self.comboBoxStandardize.setEnabled(False)

        self.tabWidget.tabBar().show()
        self.startAnalysisWidget.init(self)
        self.globalMeasuresWidget.init(Measure.GLOBAL, self.analysis)
        self.nodalMeasuresWidget.init(Measure.NODAL, self.analysis)
        self.binodalMeasuresWidget.init(Measure.BINODAL, self.analysis)

        self.init_brain_widget()
        show_only_selected = self.brain_view_options_widget.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.brain_view_options_widget.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.analysis.cohort.atlas.brain_regions, 4, [], show_brain_regions, show_only_selected)

    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getOpenFileName(self,"Open analysis", "",
                                                      "analysis files (*.analysis)", options = options)
        if file_name:
            self.from_file(file_name)
            self.start_analysis()

    def save(self):
        if self.file_name:
            self.to_file(self.file_name)
        else:
            self.save_as()

    def save_as(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, name = QFileDialog.getSaveFileName(self, "Save analysis", "untitled.analysis",
                                                      "analysis files (*.analysis)", options = options)
        if file_name:
            self.file_name = file_name
            self.to_file(file_name)

    def import_xml(self):
        pass

    def export_xml(self):
        pass

    def about(self):
        QMessageBox.about(self, 'About', 'Graph analysis editor')

    def set_weighted(self, weighted):
        self.labelBinary.setEnabled(not weighted)
        self.comboBoxBinary.setEnabled(not weighted)
        self.labelStandardize.setEnabled(weighted)
        self.comboBoxStandardize.setEnabled(weighted)
        self.analysis.set_weighted(weighted)
        self.set_graph_type()

    def set_directed(self, directed):
        self.labelSymmetrize.setEnabled(not directed)
        self.comboBoxSymmetrize.setEnabled(not directed)
        self.analysis.set_directed(directed)
        self.set_graph_type()

    def set_graph_type(self):
        self.graph_type = self.get_graph_settings().graph_class()
        self.startAnalysisWidget.init_graph_measures_widget(self.graph_type)

    def set_correlation(self, correlation_type):
        self.analysis.set_correlation(correlation_type)
        self.correlationMatrixWidget.update_correlation()

    def set_negative_rule(self, negative_rule):
        self.analysis.set_negative_rule(negative_rule)

    def set_binary_rule(self, binary_rule):
        self.analysis.set_binary_rule(binary_rule)

    def set_symmetrize_rule(self, symmetrize_rule):
        self.analysis.set_symmetrize_rule(symmetrize_rule)

    def set_standardize_rule(self, standardize_rule):
        self.analysis.set_standardize_rule(standardize_rule)

    def update_community_number(self):
        pass

    def resizeEvent(self, event):
        self.brain_view_options_widget.update_move()

    def import_error(self, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle("Import error")
        msg_box.exec_()

    def table_update_callbacks(self):
        return [widget.update_table for widget in [self.globalMeasuresWidget, self.nodalMeasuresWidget, self.binodalMeasuresWidget]]

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = GraphAnalysis()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
