from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_view_options_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BrainViewOptionsWidget(Base, Form):
    def __init__(self, parent = None):
        super(BrainViewOptionsWidget, self).__init__(parent)
        '''
        icon_location_up = abs_path_from_relative(__file__, "../icons/zoom_in.png")
        icon_location_down = abs_path_from_relative(__file__, "../icons/zoom_out.png")
        self.setStyleSheet("QGroupBox::indicator {width: 14px; height: 14px;} \
                            QGroupBox::indicator:checked {image: url({icon_location_up});} \
                            QGroupBox::indicator:Unchecked {image: url({icon_location_down});}")
        '''
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.tabWidget.hide()
        self.resize(self.sizeHint())
        self.groupBox.clicked.connect(self.update_visible)

    def update_move(self):
        self.move(0, self.parent().height()-self.height())

    def update_visible(self, visible):
        self.tabWidget.setVisible(visible)
        self.groupBox.resize(self.groupBox.sizeHint())
        self.resize(self.sizeHint())
        self.update_move()
