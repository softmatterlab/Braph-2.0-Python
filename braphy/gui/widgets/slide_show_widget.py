from PyQt5 import QtCore, QtGui, uic, QtWidgets
from braphy.gui.widgets.slide_show_3D_widget import SlideShow3DWidget
from braphy.utility.helper_functions import abs_path_from_relative

ui_file = abs_path_from_relative(__file__, "../ui_files/slide_show.ui")
Form, Base = uic.loadUiType(ui_file)

class SlideShowWidget(Base, Form):
    def __init__(self, parent = None):
        super(SlideShowWidget, self).__init__(parent)
        self.setupUi(self)
        self.label.setText('HEJ')
        self.animate = True
        self.slide_show_timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 5000 # milliseconds
        self.timerEvent()

    def init(self, color):
        self.animate = True
        self.slideShow3DWidget.init(color)
        self.btnPause.clicked.connect(self.pause_animation)

    def pause_animation(self):
        self.slideShow3DWidget.animate(not self.animate)
        self.animate = not self.animate

    def timerEvent(self, e = None):
        if not self.animate:
            return
        if self.step >= len(self.slideShow3DWidget.slides):
            self.slide_show_timer.stop()
            return
        self.slide_show_timer.start(self.delay, self)
        slide = self.slideShow3DWidget.slides[self.step]
        text = slide()
        self.label.setText(text)
        self.step += 1
        if self.step >= len(self.slideShow3DWidget.slides):
            self.step = 0
