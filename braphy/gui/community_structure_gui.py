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
        self.init_combo_box()
        self.init_buttons()
        self.init_table()

    def init_combo_box(self):
        for group in self.analysis.cohort.groups:
            self.comboBox.addItem(group.name)
        self.comboBox.currentTextChanged.connect(self.update_table)

    def init_buttons(self):
        self.btnFixed.toggled.connect(self.btn_fixed_structure)
        self.btnDynamic.toggled.connect(self.btn_dynamic_structure)
        self.btnLouvain.toggled.connect(self.btn_louvain_algorithm)
        self.btnNewman.toggled.connect(self.btn_newman_algorithm)

        self.btnSet.clicked.connect(self.btn_set)
        self.btnReset.clicked.connect(self.btn_reset)
        self.btnReset.clicked.connect(self.btn_calculate)

        self.spinBoxGamma.setValue(self.analysis.get_gamma())
        self.spinBoxGamma.valueChanged.connect(self.set_gamma)

    def init_table(self):
        self.update_table()

    def set_gamma(self, gamma):
        self.analysis.set_gamma(gamma)
        self.update_table()

    def update_table(self):
        community_structure = self.analysis.get_community_structure(self.comboBox.currentIndex())
        number_of_communities = max(community_structure) + 1
        brain_regions = self.analysis.cohort.atlas.brain_regions
        self.tableWidget.setRowCount(len(brain_regions))
        self.tableWidget.setColumnCount(1 + number_of_communities)

        for i in range(len(brain_regions)):
            region = brain_regions[i]
            item = QTableWidgetItem(region.label)
            self.tableWidget.setItem(i, 0, item)
            button_group = QButtonGroup(self)
            for j in range(number_of_communities):
                radio_button = self.get_radio_button_widget()
                if community_structure[i] == j:
                    radio_button.button.setChecked(True)
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


    def btn_fixed_structure(self):
        self.btnLouvain.setDisabled(True)
        self.btnNewman.setDisabled(True)
        self.labelGamma.setDisabled(True)
        self.textEditGamma.setDisabled(True)

    def btn_dynamic_structure(self):
        self.btnLouvain.setDisabled(False)
        self.btnNewman.setDisabled(False)
        self.labelGamma.setDisabled(False)
        self.textEditGamma.setDisabled(False)

    def btn_louvain_algorithm(self):
        print("Louvain")

    def btn_newman_algorithm(self):
        print("Newman")

    def btn_set(self):
        print("set")

    def btn_reset(self):
        print("reset")

    def btn_calculate(self):
        print("calculate")

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = CommunityStructure()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
