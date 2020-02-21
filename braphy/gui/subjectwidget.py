import os
from PyQt5 import QtGui, uic

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "ui_files/cohort_editor_subject_data_widget.ui"))

class SubjectWidget(Base, Form):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.init_buttons()

	def init_buttons(self):
		self.btnSaveSubjects.clicked.connect(self.save_subjects_as_txt)

	def save_subjects_as_txt(self):
		print("saving")

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	w = SubjectWidget()
	w.show()
	sys.exit(app.exec_())