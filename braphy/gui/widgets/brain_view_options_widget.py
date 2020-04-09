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
        self.subjects = []
        self.groups = []
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.tabWidget.hide()
        self.resize(self.sizeHint())
        self.groupBox.clicked.connect(self.update_visible)
        self.update_visible(False)
        self.init_combo_boxes()
        self.init_check_boxes()
        self.init_sliders()
        self.init_lists()

    def init(self, brain_widget):
        self.brain_widget = brain_widget
        self.settingsWidget.init(brain_widget)

    def init_combo_boxes(self):
        self.comboBoxAverageGroup.currentIndexChanged.connect(self.set_average_visualization_group)
        self.comboBoxStdGroup.currentIndexChanged.connect(self.set_std_visualization_group)
        self.comboBoxColorGroup.currentIndexChanged.connect(self.set_group_color)

        self.comboBoxAverageSubject.currentIndexChanged.connect(self.set_average_visualization_subject)
        self.comboBoxStdSubject.currentIndexChanged.connect(self.set_std_visualization_subject)
        self.comboBoxColorSubject.currentIndexChanged.connect(self.set_subject_color)

    def init_check_boxes(self):
        self.checkBoxAverageGroup.stateChanged.connect(self.visualize_average_group)
        self.checkBoxStdGroup.stateChanged.connect(self.visualize_std_group)

        self.checkBoxAverageSubject.stateChanged.connect(self.visualize_average_subject)
        self.checkBoxStdSubject.stateChanged.connect(self.visualize_std_subject)

    def init_sliders(self):
        self.horizontalSliderColorGroup.valueChanged.connect(self.set_group_color)
        self.horizontalSliderColorSubject.valueChanged.connect(self.set_subject_color)

        self.horizontalSliderSizeGroup.valueChanged.connect(self.set_group_size)
        self.horizontalSliderSizeSubject.valueChanged.connect(self.set_subject_size)

    def init_lists(self):
        self.init_subject_list()
        self.init_group_list()

    def init_subject_list(self):
        self.listWidgetSubject.blockSignals(True)
        self.listWidgetSubject.clear()
        for subject in self.subjects:
            item = QListWidgetItem(subject.id)
            self.listWidgetSubject.addItem(item)
        self.listWidgetSubject.blockSignals(False)

    def init_group_list(self):
        self.listWidgetGroup.blockSignals(True)
        self.listWidgetGroup.clear()
        for group in self.groups:
            item = QListWidgetItem(group.name)
            self.listWidgetGroup.addItem(item)
        self.listWidgetGroup.blockSignals(False)

    def set_groups(self, groups):
        self.groups = groups
        self.init_group_list()

    def set_subjects(self, subjects):
        self.subjects = subjects
        self.init_subject_list()

    def set_average_visualization_group(self):
        pass

    def set_std_visualization_group(self):
        pass

    def set_group_color(self):
        pass

    def set_average_visualization_subject(self):
        pass

    def set_std_visualization_subject(self):
        pass

    def set_subject_color(self):
        pass

    def visualize_average_group(self):
        pass

    def visualize_std_group(self):
        pass

    def set_group_size(self):
        pass

    def visualize_average_subject(self):
        pass

    def visualize_std_subject(self):
        pass

    def set_subject_size(self):
        pass

    def update_move(self):
        self.move(9, self.parent().height()-self.height() - 9)

    def update_visible(self, visible):
        if visible:
            self.tabWidget.show()
            self.groupBox.resize(self.groupBox.sizeHint())
            self.resize(self.sizeHint())
        else:
            self.tabWidget.hide()
            self.resize(80, 20)
        self.update_move()

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 3, 3)
        QWidget.paintEvent(self, e)
