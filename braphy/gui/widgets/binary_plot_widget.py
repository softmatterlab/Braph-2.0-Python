from PyQt5 import uic, Qt
from braphy.utility.file_utility import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/binary_plot_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BinaryPlotWidget(Base, Form):
    def __init__(self, parent = None):
        super(BinaryPlotWidget, self).__init__(parent)
        self.setupUi(self)
        self.plot_dict = {}
        self.info_strings = []
        self.init_buttons()
        self.listWidget.itemSelectionChanged.connect(self.selection_changed)
        self.actionLegend.triggered.connect(self.binaryPlot.show_legend)

    def init(self, analysis):
        self.binaryPlot.set_x_label(analysis.graph_settings.rule_binary)
        self.binaryMatrixPlotVisualizer.init(analysis.cohort.atlas.get_brain_region_labels(), analysis.graph_settings.rule_binary)
        self.init_combo_box(analysis.cohort.atlas.get_brain_region_labels())
        self.tabWidget.currentChanged.connect(self.tab_changed)

    def init_buttons(self):
        self.btnRemove.clicked.connect(self.remove_plot)
        self.btnClear.clicked.connect(self.clear_plot)

    def init_combo_box(self, node_labels):
        for label in node_labels:
            self.comboBox.addItem(label)
        self.comboBox.currentIndexChanged.connect(self.update_matrix_plot)

    def set_nodal(self):
        self.comboBox.hide()
        self.labelBrainRegion.hide()

    def update_matrix_plot(self, index):
        prev_title = self.binaryMatrixPlotVisualizer.get_title()
        measure = prev_title.split(',')[0]
        title = '{}, {}'.format(measure, self.comboBox.currentText())
        self.binaryMatrixPlotVisualizer.plot(self.matrix[:, index, :], title)

    def add_plot(self, info_string, values, confidence_interval):
        if info_string in self.info_strings:
            return
        self.info_strings.append(info_string)
        self.listWidget.addItem(info_string)
        self.binaryPlot.add_plot(info_string, values, confidence_interval)
        self.btnClear.setEnabled(True)

    def remove_plot(self):
        selected = self.get_selected_plots()
        for info_string in selected:
            self.binaryPlot.remove_plot(info_string)
            item = self.listWidget.findItems(info_string, Qt.Qt.MatchExactly)[0]
            self.listWidget.takeItem(self.listWidget.row(item))
            self.info_strings.remove(info_string)

    def clear_plot(self):
        self.binaryPlot.clear_plot()
        self.plot_dict = {}
        self.info_strings = []
        self.listWidget.clear()
        self.btnClear.setEnabled(False)
        self.actionLegend.setChecked(False)

    def get_selected_plots(self):
        items = self.listWidget.selectedItems()
        items_text = [item.text() for item in items]
        return items_text

    def selection_changed(self):
        items_text = self.get_selected_plots()
        if len(items_text) > 0:
            self.btnRemove.setEnabled(True)
        else:
            self.btnRemove.setEnabled(False)

    def get_actions(self):
        actions = [self.actionLegend, self.actionShow_labels, self.actionShow_colorbar, self.actionInspect]
        actions.extend(self.binaryPlot.get_actions())
        actions.extend(self.binaryMatrixPlotVisualizer.get_actions())
        return actions

    def get_tab_index(self):
        return self.tabWidget.currentIndex()

    def tab_changed(self):
        if self.tabWidget.currentIndex() == 0:
            self.set_plot_actions_visible(True)
            self.set_matrix_actions_visible(False)
        elif self.tabWidget.currentIndex() == 1:
            self.set_plot_actions_visible(False)
            self.set_matrix_actions_visible(True)

    def set_matrix_actions_visible(self, state):
        matrix_actions = [self.actionShow_labels, self.actionShow_colorbar, self.actionInspect]
        matrix_actions.extend(self.binaryMatrixPlotVisualizer.get_actions())
        for action in matrix_actions:
            action.setVisible(state)

    def set_plot_actions_visible(self, state):
        actions  = [self.actionLegend]
        actions.extend(self.binaryPlot.get_actions())
        for action in actions:
            action.setVisible(state)

    def show_actions(self, state):
        if not state:
            self.set_matrix_actions_visible(False)
            self.set_plot_actions_visible(False)
        else:
            self.tab_changed()