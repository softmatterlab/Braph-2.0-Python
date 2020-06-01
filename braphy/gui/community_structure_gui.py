import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QRadioButton, QTableWidgetItem, QButtonGroup
from braphy.utility.helper_functions import abs_path_from_relative

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/community_structure.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CommunityStructure(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, analysis, AppWindow = None):
        if AppWindow:
            self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.analysis = analysis
        self.read_only = False
        self.init_combo_box()
        self.init_buttons()
        self.init_table()
        self.init_actions()

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBox.addItem(group.name)
        self.comboBox.currentTextChanged.connect(lambda signal: self.update_table)

    def init_buttons(self):
        self.btnFixed.toggled.connect(self.fixed_structure)
        self.btnDynamic.toggled.connect(self.dynamic_structure)
        self.btnLouvain.toggled.connect(self.louvain_algorithm)
        self.btnNewman.toggled.connect(self.newman_algorithm)
        self.btnHidden = QRadioButton()
        self.btnHidden.hide()

        button_group = QButtonGroup(self)
        for item in [self.btnFixed, self.btnDynamic]:
            button_group.addButton(item)
        button_group = QButtonGroup(self)
        for item in [self.btnLouvain, self.btnNewman, self.btnHidden]:
            button_group.addButton(item)

        self.btnSet.clicked.connect(self.set_community_structure)
        self.btnReset.clicked.connect(self.reset_community_structure)

        self.spinBoxGamma.setValue(self.analysis.get_gamma())
        self.spinBoxGamma.valueChanged.connect(self.set_gamma)

    def init_table(self):
        self.update_table(self.analysis.community_structure)

    def init_actions(self):
        for action in self.brainWidget.get_actions():
            self.toolBar.addAction(action)

    def set_gamma(self, gamma):
        self.analysis.set_gamma(gamma)
        self.update_table()

    def update_table(self, community_structure = None):
        if community_structure is None:
            community_structure = self.analysis.get_community_structure(self.comboBox.currentIndex())
        self.community_structure = community_structure.copy()
        number_of_communities = max(self.community_structure) + 1
        brain_regions = self.analysis.cohort.atlas.brain_regions
        self.tableWidget.setRowCount(len(brain_regions))
        self.tableWidget.setColumnCount(2 + number_of_communities)
        headers = ['Brain region']
        headers = headers + [str(community_number) for community_number in range(number_of_communities+1)]
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for i in range(len(brain_regions)):
            region = brain_regions[i]
            item = QTableWidgetItem(region.label)
            if self.read_only:
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            else:
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
        for community in range(max(self.community_structure)):
            if community not in self.community_structure:
                for i in range(len(self.community_structure)):
                    if self.community_structure[i] > community:
                        self.community_structure[i] -= 1

    def fixed_structure(self):
        self.btnHidden.setChecked(True)
        disabled_items = [self.btnLouvain, self.btnNewman,
                          self.labelGamma, self.spinBoxGamma]
        for item in disabled_items:
            item.setDisabled(True)
        self.read_only = False
        self.update_table(self.community_structure)
        self.tableWidget.setEnabled(True)

    def dynamic_structure(self):
        disabled_items = [self.btnLouvain, self.btnNewman,
                          self.labelGamma, self.spinBoxGamma]
        for item in disabled_items:
            item.setEnabled(True)
        self.read_only = True
        self.update_table()

    def louvain_algorithm(self):
        pass

    def newman_algorithm(self):
        pass

    def set_community_structure(self):
        self.analysis.community_structure = self.community_structure.copy()

    def reset_community_structure(self):
        self.update_table(self.analysis.community_structure)

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CommunityStructure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
