import os
from braphy.utility.helper_functions import abs_path_from_relative
from PyQt5 import QtGui, uic

Form, Base = uic.loadUiType(abs_path_from_relative(__file__, "ui_files/cohort_editor_group_averages_widget.ui"))

class BrainWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
        self.btnViewSubjects.clicked.connect(self.view_subjects)
        self.btnViewGroup.clicked.connect(self.view_group)
        self.btnViewComparison.clicked.connect(self.view_comparison)

    def view_subjects(self):
        print("view subjects")

    def view_group(self):
        print("view group")

    def view_comparison(self):
        print("view comparison")

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = BrainWidget()
    w.show()
    sys.exit(app.exec_())
