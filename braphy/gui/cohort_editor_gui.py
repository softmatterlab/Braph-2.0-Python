import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import *#QFileDialog, QTableWidget, QTableWidgetItem, QRadioButton, QWidget, 
from braphy.utility.helper_functions import abs_path_from_relative
from functools import partial
import xml.etree.ElementTree as ET

qtCreatorFile = abs_path_from_relative(__file__, "ui_files/cohort_editor.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CohortEditor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, AppWindow):
        self.AppWindow = AppWindow
        QtWidgets.QMainWindow.__init__(self, parent = None)
        self.setupUi(self)
        self.init_buttons()
        self.init_actions()
        self.init_table()
        self.atlas_loaded = False
        self.disable_menu_bar(True)

    def init_table(self):
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)

    def init_buttons(self):
        self.btnAtlas.clicked.connect(self.btn_brain_atlas)

        self.btnLoadXls.clicked.connect(self.load_xls_subject_group)
        self.btnLoadTxt.clicked.connect(self.load_txt_subject_group)
        self.btnLoadXml.clicked.connect(self.load_xml_subject_group)

        self.btnAdd.clicked.connect(self.add_new_group)
        self.btnRemove.clicked.connect(self.remove_group)
        self.btnMoveUp.clicked.connect(self.move_group_up)
        self.btnMoveDown.clicked.connect(self.move_group_down)

        self.btnInvert.clicked.connect(self.invert_group)
        self.btnMerge.clicked.connect(self.merge_groups)
        self.btnIntersect.clicked.connect(self.intersect_groups)

        self.btnGroupPage.clicked.connect(self.group_page)
        self.btnSubjectPage.clicked.connect(self.subject_page)
        self.btnAveragesPage.clicked.connect(self.averages_page)
        self.btnBrainPage.clicked.connect(self.brain_page)

    def group_page(self):
        self.stackedWidget.setCurrentIndex(0)
        self.set_brain_view_actions_visible(False)

    def subject_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.set_brain_view_actions_visible(False)

    def averages_page(self):
        self.stackedWidget.setCurrentIndex(2)
        self.set_brain_view_actions_visible(False)

    def brain_page(self):
        self.stackedWidget.setCurrentIndex(3)
        self.set_brain_view_actions_visible(True)

    def init_actions(self):
        self.actionOpen.triggered.connect(self.open)
        self.set_brain_view_actions_visible(False)

    def set_brain_view_actions_visible(self, state):
        self.actionZoom_in.setVisible(state)
        self.actionZoom_out.setVisible(state)
        self.actionPan.setVisible(state)
        self.action3D_rotation.setVisible(state)
        self.actionData_cursor.setVisible(state)
        self.actionInsert_colorbar.setVisible(state)
        self.action3D.setVisible(state)
        self.actionSagittal_left.setVisible(state)
        self.actionSagittal_right.setVisible(state)
        self.actionAxial_dorsal.setVisible(state)
        self.actionAxial_ventral.setVisible(state)
        self.actionCoronal_anterior.setVisible(state)
        self.actionCoronal_posterior.setVisible(state)
        self.actionBrain.setVisible(state)
        self.actionShow_axis.setVisible(state)
        self.actionShow_grid.setVisible(state)
        self.actionShow_symbols.setVisible(state)
        self.actionRegions.setVisible(state)
        self.actionShow_labels.setVisible(state)

    def open(self):
        print("open")

    def btn_brain_atlas(self):
        self.load_atlas()
        self.atlas_loaded = True
        self.btnAtlas.setText("View Atlas")
        self.disable_menu_bar(False)

    def load_atlas(self):
        print("Loading brain atlas...")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","atlas files (*.atlas)", options=options)
        if fileName:
            print(fileName)

    def load_xls_subject_group(self):
        print("Loading xls subject group...")

    def load_txt_subject_group(self):
        print("Loading txt subject group...")

    def load_xml_subject_group(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, name = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","xml files (*.xml)", options=options)
        if fileName:
            tree = ET.parse(fileName)
            root = tree.getroot()
            subjects = []
            for MRISubject in root[0].findall('MRISubject'):
                tmp_dict = {
                    "age": MRISubject.attrib["age"],
                    "code": MRISubject.attrib["code"],
                    "data": self.string_to_list_of_floats(MRISubject.attrib["data"]),
                    "gender": MRISubject.attrib["gender"],
                    "notes": MRISubject.attrib["notes"]
                }
                subjects.append(tmp_dict)
            group_data = {
                "data": self.string_to_list_of_ints(root[0][-1][0].attrib["data"]),
                "name": root[0][-1][0].attrib["name"],
                "notes": root[0][-1][0].attrib["notes"]
            }
            self.subjects = subjects
            self.group_data = group_data
            self.update_table()

    def string_to_list_of_floats(self, str):
        string_list = str.split()
        float_list = []
        for i in string_list:
            float_list.append(float(i))
        return float_list

    def string_to_list_of_ints(self, str):
        string_list = str.split()
        float_list = []
        for i in string_list:
            float_list.append(int(i))
        return float_list

    def update_table(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        radio_button = QRadioButton()
        radio_button.setChecked(False)
        layout.addWidget(radio_button)
        widget.setLayout(layout)
        self.tableWidget.setCellWidget(0, 0, widget)

        item = QTableWidgetItem(self.group_data["name"])
        self.tableWidget.setItem(0, 1, item)

        item = QTableWidgetItem(str(len(self.group_data["data"])))
        self.tableWidget.setItem(0, 2, item)

        item = QTableWidgetItem(self.group_data["notes"])
        self.tableWidget.setItem(0, 3, item)

    def disable_menu_bar(self, b):
        self.menuGroups.setDisabled(b)
        self.menuSubjects.setDisabled(b)
        self.menuView.setDisabled(b)
        self.menuBrain_View.setDisabled(b)
        self.menuGraph_Analysis.setDisabled(b)

    def add_new_group(self):
        print("Add group")
    
    def remove_group(self):
        print("remove group")

    def move_group_up(self):
        print("Move up")

    def move_group_down(self):
        print("Move down")

    def invert_group(self):
        print("invert")

    def merge_groups(self):
        print("merge")

    def intersect_groups(self):
        print("intersect")

def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = CohortEditor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
