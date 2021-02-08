from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtGui import QIcon
from GUI.hello import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI.login_ui import *

class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(519, 227)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(310, 120, 51, 21))
        self.login_btn.setObjectName("login_btn")
        self.account_le = QtWidgets.QLineEdit(self.centralwidget)
        self.account_le.setGeometry(QtCore.QRect(310, 60, 151, 20))
        self.account_le.setText("")
        self.account_le.setPlaceholderText("")
        self.account_le.setObjectName("account_le")
        self.password_le = QtWidgets.QLineEdit(self.centralwidget)
        self.password_le.setGeometry(QtCore.QRect(310, 90, 151, 20))
        self.password_le.setText("")
        self.password_le.setPlaceholderText("")
        self.password_le.setObjectName("password_le")
        self.cancel_btn = QtWidgets.QPushButton(self.centralwidget)
        self.cancel_btn.setGeometry(QtCore.QRect(410, 120, 51, 21))
        self.cancel_btn.setObjectName("Cancel_btn")
        self.camera_btn = QtWidgets.QPushButton(self.centralwidget)
        self.camera_btn.setGeometry(QtCore.QRect(80, 60, 111, 81))
        self.camera_btn.setObjectName("Camera_btn")
        self.account_lb = QtWidgets.QLabel(self.centralwidget)
        self.account_lb.setGeometry(QtCore.QRect(220, 60, 71, 20))
        self.account_lb.setObjectName("account_lb")
        self.password_lb = QtWidgets.QLabel(self.centralwidget)
        self.password_lb.setGeometry(QtCore.QRect(220, 90, 71, 20))
        self.password_lb.setObjectName("password_lb")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 519, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.login_btn.clicked.connect(self.word_get)
        self.camera_btn.clicked.connect(self.face_get)
        self.cancel_btn.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LOGIN"))
        self.login_btn.setText(_translate("MainWindow", "Login"))
        self.cancel_btn.setText(_translate("MainWindow", "Cancel"))
        self.camera_btn.setText(_translate("MainWindow", "Login By Camera"))
        self.account_lb.setText(_translate("MainWindow", "Account"))
        self.password_lb.setText(_translate("MainWindow", "Password"))
        self.account_le.setPlaceholderText(_translate("MainWindow", "Please Input Username"))
        self.password_le.setPlaceholderText(_translate("MainWindow", "Please Input Password"))

    def word_get(self):
        login_user = self.account_le.text()
        login_password = self.password_le.text()

        if login_user == 'admin' and login_password == '123456':
            ui_hello.show()
            MainWindow.close()
        else:
            QMessageBox.warning(self,
                    "Warning",
                    "Wrong username or password. Try again.",
                    QMessageBox.Yes)
            self.account_le.setFocus()

    def face_get(self):
        from FaceRecognition import person_reidentification
        person_name = person_reidentification.face_recognition()
        # while person_reidentification.face_recognition() == False:
        #     person_name =
        #     break
        if person_name == False:
            return 0

        QMessageBox.information(self, 'Info', 'Welcome! ' + person_name, QMessageBox.Ok)


        ui_hello.show()
        MainWindow.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui_hello = hello_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())