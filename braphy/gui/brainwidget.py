import os
from PyQt5 import QtGui, uic

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "ui_files/cohort_editor_brain_view_widget.ui"))

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