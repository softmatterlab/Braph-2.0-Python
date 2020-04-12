from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import numpy as np
from braphy.utility.helper_functions import abs_path_from_relative, QColor_to_list, QColor_from_list

ui_file = abs_path_from_relative(__file__, "../ui_files/brain_atlas_settings_widget.ui")
Form, Base = uic.loadUiType(ui_file)

class BrainAtlasSettingsWidget(Base, Form):
    def __init__(self, parent = None):
        super(BrainAtlasSettingsWidget, self).__init__(parent)
        self.setupUi(self)

    def init(self, brain_widget):
        self.brain_widget = brain_widget
        self.init_combo_boxes()
        self.init_sliders()
        self.init_buttons()
        self.init_check_boxes()
        self.init_actions()

    def init_combo_boxes(self):
        shaders = ['shaded', 'normalColor', 'balloon', 'viewNormalColor', 'edgeHilight', 'pointSprite']
        for shader in shaders:
            self.comboBoxMesh.addItem(shader)
        self.comboBoxMesh.currentIndexChanged.connect(self.set_brain_mesh_shader)
        self.comboBoxMesh.setCurrentText('normalColor')

    def init_sliders(self):
        self.sliderBrain.valueChanged.connect(self.change_transparency)
        self.sliderBrain.setValue(50)
        self.sliderRegions.valueChanged.connect(self.change_brain_region_size)

    def init_buttons(self):
        self.btnRegions.clicked.connect(self.pick_brain_region_color)
        self.btnRegionsSelected.clicked.connect(self.pick_selected_brain_region_color)
        self.init_brain_region_color()

        self.btn3D.clicked.connect(self.brain_widget.show_3D)
        self.btnSagittalLeft.clicked.connect(self.brain_widget.sagittal_left)
        self.btnSagittalRight.clicked.connect(self.brain_widget.sagittal_right)
        self.btnAxialDorsal.clicked.connect(self.brain_widget.axial_dorsal)
        self.btnAxialVentral.clicked.connect(self.brain_widget.axial_ventral)
        self.btnCoronalAnterior.clicked.connect(self.brain_widget.coronal_anterior)
        self.btnCoronalPosterior.clicked.connect(self.brain_widget.coronal_posterior)

    def init_brain_region_color(self):
        style_sheet = 'background-color: {};'.format(QColor_from_list(self.brain_widget.region_color).name())
        self.btnRegions.setStyleSheet(style_sheet)
        style_sheet = 'background-color: {};'.format(QColor_from_list(self.brain_widget.selected_region_color).name())
        self.btnRegionsSelected.setStyleSheet(style_sheet)

    def init_check_boxes(self):
        self.checkBoxShowBrainRegions.stateChanged.connect(self.show_brain_regions)
        self.checkBoxShowBrainRegions.setChecked(True)
        self.checkBoxShowBrain.stateChanged.connect(self.show_brain)
        self.checkBoxShowBrain.setChecked(True)
        self.checkBoxShowAxis.stateChanged.connect(self.show_axis)
        self.checkBoxShowAxis.setChecked(True)
        self.checkBoxShowGrid.stateChanged.connect(self.show_grid)
        self.checkBoxShowGrid.setChecked(True)
        self.checkBoxShowLabels.stateChanged.connect(self.show_labels)
        self.checkBoxShowLabels.setChecked(True)
        self.checkBoxShowOnlySelected.stateChanged.connect(self.show_only_selected)

    def init_actions(self):
        self.action3D.triggered.connect(self.brain_widget.show_3D)
        self.actionSagittal_left.triggered.connect(self.brain_widget.sagittal_left)
        self.actionSagittal_right.triggered.connect(self.brain_widget.sagittal_right)
        self.actionAxial_dorsal.triggered.connect(self.brain_widget.axial_dorsal)
        self.actionAxial_ventral.triggered.connect(self.brain_widget.axial_ventral)
        self.actionCoronal_anterior.triggered.connect(self.brain_widget.coronal_anterior)
        self.actionCoronal_posterior.triggered.connect(self.brain_widget.coronal_posterior)

        self.actionShow_brain.triggered.connect(self.show_brain)
        self.actionShow_brain.setChecked(True)
        self.actionShow_axis.triggered.connect(self.show_axis)
        self.actionShow_axis.setChecked(True)
        self.actionShow_grid.triggered.connect(self.show_grid)
        self.actionShow_grid.setChecked(True)
        self.actionShow_brain_regions.triggered.connect(self.show_brain_regions)
        self.actionShow_brain_regions.setChecked(True)
        self.actionShow_labels.triggered.connect(self.show_labels)
        self.actionShow_labels.setChecked(True)

    def get_actions(self):
        actions = [self.action3D, self.actionSagittal_left, self.actionSagittal_right,
                   self.actionAxial_dorsal, self.actionAxial_ventral, self.actionCoronal_anterior,
                   self.actionCoronal_posterior, self.actionShow_brain, self.actionShow_axis,
                   self.actionShow_grid, self.actionShow_brain_regions, self.actionShow_labels]
        return actions

    def show_brain(self, state):
        if (self.actionShow_brain.isChecked() != self.checkBoxShowBrain.isChecked()):
            self.brain_widget.show_brain(state)
            self.actionShow_brain.setChecked(state != 0)
            self.checkBoxShowBrain.setChecked(state != 0)

    def show_axis(self, state):
        if (self.actionShow_axis.isChecked() != self.checkBoxShowAxis.isChecked()):
            self.brain_widget.show_axis(state)
            self.actionShow_axis.setChecked(state != 0)
            self.checkBoxShowAxis.setChecked(state != 0)

    def show_grid(self, state):
        if (self.actionShow_grid.isChecked() != self.checkBoxShowGrid.isChecked()):
            self.brain_widget.show_grid(state)
            self.actionShow_grid.setChecked(state != 0)
            self.checkBoxShowGrid.setChecked(state != 0)

    def show_brain_regions(self, state):
        if (self.actionShow_brain_regions.isChecked() != self.checkBoxShowBrainRegions.isChecked()):
            self.brain_widget.set_brain_regions_visible(state != 0)
            self.actionShow_brain_regions.setChecked(state != 0)
            self.checkBoxShowBrainRegions.setChecked(state != 0)
            if state == 0:
                self.checkBoxShowLabels.setChecked(False)
                self.checkBoxShowLabels.setEnabled(False)
                self.checkBoxShowOnlySelected.setChecked(False)
                self.checkBoxShowOnlySelected.setEnabled(False)
            else:
                self.checkBoxShowLabels.setEnabled(True)
                self.checkBoxShowOnlySelected.setEnabled(True)

    def show_labels(self, state):
        if (self.actionShow_labels.isChecked() != self.checkBoxShowLabels.isChecked()):
            self.brain_widget.show_labels(state)
            self.actionShow_labels.setChecked(state != 0)
            self.checkBoxShowLabels.setChecked(state != 0)

    def show_only_selected(self, state):
        self.brain_widget.show_only_selected = (state != 0)
        self.brain_widget.update_brain_regions_plot()

    def pick_color(self):
        options = QtWidgets.QColorDialog.ColorDialogOptions()
        options |= QtWidgets.QColorDialog.DontUseNativeDialog
        return QtWidgets.QColorDialog.getColor(options = options)

    def pick_brain_region_color(self):
        color = self.pick_color()
        if color.isValid():
            self.set_brain_region_color(color)

    def set_brain_region_color(self, color):
        style_sheet = 'background-color: {};'.format(color.name())
        self.btnRegions.setStyleSheet(style_sheet)
        self.brain_widget.set_brain_region_color(QColor_to_list(color))

    def pick_selected_brain_region_color(self):
        color = self.pick_color()
        if color.isValid():
            self.set_selected_brain_region_color(color)

    def set_selected_brain_region_color(self, color):
        style_sheet = 'background-color: {};'.format(color.name())
        self.btnRegionsSelected.setStyleSheet(style_sheet)
        self.brain_widget.set_selected_brain_region_color(QColor_to_list(color))

    def change_transparency(self):
        alpha = self.sliderBrain.value()/100.0
        self.brain_widget.change_transparency(alpha)

    def set_brain_mesh_shader(self):
        self.brain_widget.set_shader(self.comboBoxMesh.currentText())

    def change_brain_region_size(self):
        size = self.sliderRegions.value()/10.0
        self.brain_widget.change_brain_region_size(size)
