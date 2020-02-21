import os
from PyQt5 import QtGui, uic

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = uic.loadUiType(os.path.join(current_dir, "ui_files/cohort_editor_group_demographics_widget.ui"))

class GroupWidget(Base, Form):
	def __init__(self, parent=None):
		super(self.__class__, self).__init__(parent)
		self.setupUi(self)
		self.init_buttons()

	def init_buttons(self):
		self.btnSelectAll.clicked.connect(self.select_all)
		self.btnClearSelection.clicked.connect(self.clear_selection)
		self.btnAddSubject.clicked.connect(self.add_subject)
		self.btnAddAbove.clicked.connect(self.add_above)
		self.btnAddBelow.clicked.connect(self.add_below)
		self.btnRemove.clicked.connect(self.remove)
		self.btnMoveUp.clicked.connect(self.move_up)
		self.btnMoveDown.clicked.connect(self.move_down)
		self.btnMoveToTop.clicked.connect(self.move_to_top)
		self.btnMoveToBottom.clicked.connect(self.move_to_bottom)
		self.btnNewGroup.clicked.connect(self.new_group)

	def select_all(self):
		print("select all")

	def clear_selection(self):
    		print("clear")

	def add_subject(self):
    		print("add")

	def add_above(self):
    		print("above")

	def add_below(self):
    		print("below")

	def remove(self):
    		print("remove")

	def move_up(self):
    		print("up")

	def move_down(self):
    		print("down")

	def move_to_top(self):
    		print("top")

	def move_to_bottom(self):
    		print("bottom")

	def new_group(self):
    		print("new group")

if __name__ == '__main__':
	import sys
	app = QtGui.QApplication(sys.argv)
	w = GroupWidget()
	w.show()
	sys.exit(app.exec_())