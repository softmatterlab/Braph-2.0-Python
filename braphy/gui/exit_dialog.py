from PyQt5 import QtWidgets

class ExitDialog(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message', "Are you sure you want to quit, buddy?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
