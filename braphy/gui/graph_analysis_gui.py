import sys
import json
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *
from braphy.graph.graphs import *
from braphy.graph.measures.measure import Measure
from braphy.workflows import *
from braphy.cohort.cohort import Cohort
from braphy.gui.cohort_editor_gui import CohortEditor
from braphy.analysis.analysis import Analysis
from braphy.gui.community_structure_gui import CommunityStructure
from braphy.gui.widgets.brain_view_options_widget import BrainViewOptionsWidget
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/graph_analysis.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class GraphAnalysis(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow = None, subject_class = SubjectMRI):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)

        self.init_buttons()
        self.init_actions()
        self.init_comboboxes()
        self.graphMeasuresWidget.init()
        self.startAnalysisWidget.hide()
        self.tabWidget.tabBar().hide()
        self.tabWidget.currentChanged.connect(self.tab_changed)

        if subject_class == SubjectMRI:
            self.correlationMatrixWidget.set_structural_view()
            self.repetitionLabel.hide()
            self.setWindowTitle('MRI Graph Analysis')
            self.analysis_class = AnalysisMRI
        elif subject_class == SubjectfMRI:
            self.setWindowTitle('fMRI Graph Analysis')
            self.analysis_class = AnalysisfMRI

        self.subject_class = subject_class
        self.btnViewCohort.setEnabled(False)
        self.analysis = None
        self.textAnalysisName.textChanged.connect(self.set_analysis_name)
        self.set_locked(True)

        self.brain_view_options_widget = BrainViewOptionsWidget(parent=self.tabBrainView)
        self.brain_view_options_widget.raise_()

    def set_locked(self, locked):
        lock_items = [self.correlationMatrixWidget, self.graphMeasuresWidget, self.textAnalysisName,
                      self.comboBoxGraph, self.comboBoxCorrelation, self.comboBoxNegative, self.comboBoxBinary,
                      self.btnSubgraphAnalysis, self.btnStartAnalysis, self.groupBoxCommunityStructure]
        for item in lock_items:
            item.setEnabled(not locked)

    def init_buttons(self):
        self.btnSelectCohort.clicked.connect(self.select_cohort)
        self.btnViewCohort.clicked.connect(self.view_cohort)
        self.btnEdit.clicked.connect(self.edit_community)
        self.btnDefault.clicked.connect(self.default)
        self.btnSubgraphAnalysis.clicked.connect(self.subgraph_analysis)
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

    def init_comboboxes(self):
        graphs = ['weighted undirected', 'weighted directed', 'binary undirected', 'binary directed']
        correlations = ['pearson', 'spearman', 'kendall', 'partial pearson', 'partial spearman']
        rules = ['zero', 'none', 'abs']
        binary = ['threshold', 'density']
        self.comboBoxGraph.addItems(graphs)
        self.comboBoxCorrelation.addItems(correlations)
        self.comboBoxNegative.addItems(rules)
        self.comboBoxBinary.addItems(binary)

        self.comboBoxGraph.currentTextChanged.connect(self.set_graph_type)
        self.comboBoxCorrelation.currentTextChanged.connect(self.set_correlation)
        self.comboBoxNegative.currentTextChanged.connect(self.set_negative_rule)
        self.comboBoxBinary.currentTextChanged.connect(self.set_binary_rule)

    def tab_changed(self):
        if self.tabWidget.currentIndex() == 0:
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(True)
        elif self.tabWidget.currentIndex() == 1:
            self.globalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
        elif self.tabWidget.currentIndex() == 2:
            self.nodalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
        elif self.tabWidget.currentIndex() == 3:
            self.binodalMeasuresWidget.update_table()
            self.set_brain_view_actions_visible(False)
            self.set_correlation_actions_visible(False)
        elif self.tabWidget.currentIndex() == 4:
            self.set_brain_view_actions_visible(True)
            self.set_correlation_actions_visible(False)
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
                if cohort.subject_class != self.subject_class:
                    self.import_error('Wrong data type. Load a cohort with subjects of type {} instead.'.format(self.subject_class.__name__))
                    return
            analysis = self.analysis_class(cohort)
            self.textAnalysisName.setText(analysis.name)
            self.btnViewCohort.setEnabled(True)
            self.set_locked(False)
            self.analysis = analysis
            self.analysis.set_correlation(self.comboBoxCorrelation.currentText())
            self.analysis.set_negative_rule(self.comboBoxNegative.currentText())
            self.analysis.set_binary_rule(self.comboBoxBinary.currentText())
            self.set_graph_type(self.comboBoxGraph.currentText())
            self.correlationMatrixWidget.init(analysis)
            self.set_cohort_labels()
            self.init_correlation_matrix_actions()
            self.init_brain_view_actions()
            self.update_gamma()
            self.update_community_number()

    def set_cohort_labels(self):
        self.subjectLabel.setText('Number of subjects = {}'.format(len(self.analysis.cohort.subjects)))
        self.groupLabel.setText('Number of groups = {}'.format(len(self.analysis.cohort.groups)))

    def view_cohort(self):
        self.cohort_editor_gui = CohortEditor(self, self.subject_class, self.analysis.cohort, brain_mesh_data = self.brain_mesh_data)
        self.cohort_editor_gui.set_read_only()
        self.cohort_editor_gui.show()

    def edit_community(self):
        self.community_structure_gui = CommunityStructure(self.analysis, self.brain_mesh_data, AppWindow = self)
        self.community_structure_gui.spinBoxGamma.valueChanged.connect(self.update_gamma)
        self.community_structure_gui.show()

    def default(self):
        pass

    def subgraph_analysis(self):
        pass

    def start_analysis(self):
        self.groupBoxCommunityStructure.hide()
        self.startAnalysisWidget.show()
        self.btnStartAnalysis.hide()
        self.btnSubgraphAnalysis.hide()
        self.graphMeasuresWidget.hide()

        self.comboBoxCorrelation.setEnabled(False)
        self.comboBoxGraph.setEnabled(False)
        self.comboBoxNegative.setEnabled(False)

        self.tabWidget.tabBar().show()
        self.startAnalysisWidget.init(self.graph_type, self, self.analysis)
        self.globalMeasuresWidget.init(Measure.GLOBAL, self.analysis)
        self.nodalMeasuresWidget.init(Measure.NODAL, self.analysis)
        self.binodalMeasuresWidget.init(Measure.BINODAL, self.analysis)

        self.brainWidget.set_brain_mesh(self.brain_mesh_data)
        show_only_selected = self.brain_view_options_widget.settingsWidget.checkBoxShowOnlySelected.isChecked()
        show_brain_regions = self.brain_view_options_widget.settingsWidget.actionShow_brain_regions.isChecked()
        self.brainWidget.init_brain_regions(self.analysis.cohort.atlas.brain_regions, 4, [], show_brain_regions, show_only_selected)

        self.brain_view_options_widget.init(self.brainWidget)
        self.brain_view_options_widget.settingsWidget.change_transparency()
        self.brain_view_options_widget.set_graph_view_mode()
        self.brain_view_options_widget.show()
        self.brain_view_options_widget.graphViewWidget.set_analysis(self.analysis)

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def import_xml(self):
        pass

    def export_xml(self):
        pass

    def about(self):
        QMessageBox.about(self, 'About', 'Graph analysis editor')

    def set_graph_type(self, graph_type):
        self.graph_type = GraphAnalysis.graph_cls_from_str(graph_type)
        self.graphMeasuresWidget.update_measure_list(self.graph_type)
        self.analysis.set_graph_type(self.graph_type)
        self.correlationMatrixWidget.update_graphics_view()
        if self.graph_type.weighted:
            self.labelBinary.setEnabled(False)
            self.comboBoxBinary.setEnabled(False)
        else:
            self.labelBinary.setEnabled(True)
            self.comboBoxBinary.setEnabled(True)

    def set_correlation(self, correlation_type):
        self.analysis.set_correlation(correlation_type)
        self.correlationMatrixWidget.update_graphics_view()

    def set_negative_rule(self, negative_rule):
        self.analysis.set_negative_rule(negative_rule)
        self.correlationMatrixWidget.update_graphics_view()

    def set_binary_rule(self, binary_rule):
        self.analysis.set_binary_rule(binary_rule)

    def update_gamma(self):
        self.labelGamma.setText('gamma = {}'.format(self.analysis.get_gamma()))

    def update_community_number(self):
        self.labelCommunity.setText('community number = {}'.format(self.analysis.number_of_communities()))

    def resizeEvent(self, event):
        self.brain_view_options_widget.update_move()

    def import_error(self, msg):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle("Import error")
        msg_box.exec_()

    def graph_cls_from_str(s):
        graph_type = None
        if s == 'binary undirected':
            graph_type = GraphBU
        elif s == 'binary directed':
            graph_type = GraphBD
        elif s == 'weighted undirected':
            graph_type = GraphWU
        elif s == 'weighted directed':
            graph_type = GraphWD
        return graph_type

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = GraphAnalysis()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
