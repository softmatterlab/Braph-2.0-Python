from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
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
        self.visualization_options = ['Color', 'Size']
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
        for option in self.visualization_options:
            self.comboBoxAverageGroup.addItem(option)
            self.comboBoxStdGroup.addItem(option)
        self.comboBoxAverageGroup.setCurrentIndex(-1)
        self.comboBoxStdGroup.setCurrentIndex(-1)

        self.comboBoxColorGroup.addItem('colormap hsv')

        self.comboBoxAverageGroup.currentIndexChanged.connect(self.set_average_visualization_group)
        self.comboBoxStdGroup.currentIndexChanged.connect(self.set_std_visualization_group)
        self.comboBoxColorGroup.currentIndexChanged.connect(self.set_group_color)

        self.comboBoxAverageSubject.currentIndexChanged.connect(self.set_average_visualization_subject)
        self.comboBoxStdSubject.currentIndexChanged.connect(self.set_std_visualization_subject)
        self.comboBoxColorSubject.currentIndexChanged.connect(self.set_subject_color)

        self.comboBoxAverageGroup.setEnabled(False)
        self.comboBoxStdGroup.setEnabled(False)
        self.comboBoxAverageSubject.setEnabled(False)
        self.comboBoxStdSubject.setEnabled(False)

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

    def set_average_visualization_group(self, index): # combo box
        if self.comboBoxStdGroup.currentIndex() == index:
            self.comboBoxStdGroup.blockSignals(True)
            self.comboBoxStdGroup.setCurrentIndex(-1)
            self.comboBoxStdGroup.blockSignals(False)

        self.set_visualization()

    def set_std_visualization_group(self, index): # combo box
        if self.comboBoxAverageGroup.currentIndex() == index:
            self.comboBoxAverageGroup.blockSignals(True)
            self.comboBoxAverageGroup.setCurrentIndex(-1)
            self.comboBoxAverageGroup.blockSignals(False)

    def set_group_color(self):
        pass

    def set_average_visualization_subject(self):
        pass

    def set_std_visualization_subject(self):
        pass

    def set_subject_color(self):
        pass

    def visualize_average_group(self, state): # check box
        self.comboBoxAverageGroup.setEnabled(state)

    def visualize_std_group(self, state): # check box
        self.comboBoxStdGroup.setEnabled(state)

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

    def set_visualization(self):
        if self.checkBoxAverageGroup.isChecked():
            current_group = self.groups[self.listWidgetGroup.currentRow()]
            averages = current_group.averages()
            average_min = np.min(averages)
            average_max = np.max(averages)
            averages = (averages-average_min)/(average_max - average_min)
            visualization_type = self.comboBoxAverageGroup.currentText()
            if visualization_type == 'Color':
                for i, region in enumerate(self.brain_widget.gui_brain_regions):
                    region.setColor([averages[i], averages[i], averages[i], 1.0])

        if self.checkBoxstdGroup.isChecked():
            pass


