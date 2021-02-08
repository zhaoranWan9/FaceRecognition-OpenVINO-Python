from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.main_ui import *
class hello_mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(hello_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = hello_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())