import os
from braphy.utility.helper_functions import abs_path_from_relative
from PyQt5 import QtGui, uic

Form, Base = uic.loadUiType(abs_path_from_relative(__file__, "ui_files/cohort_editor_group_averages_widget.ui"))

class AveragesWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.init_buttons()

    def init_buttons(self):
        self.btnComparison.clicked.connect(self.comparison)

    def comparison(self):
        print("comparison")

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = AveragesWidget()
    w.show()
    sys.exit(app.exec_())
