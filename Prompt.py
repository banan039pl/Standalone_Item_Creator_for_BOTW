# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prompt.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(482, 213)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.OkButton = QtWidgets.QPushButton(self.frame)
        self.OkButton.setObjectName("OkButton")
        self.gridLayout.addWidget(self.OkButton, 1, 0, 1, 1)
        self.YesButton = QtWidgets.QPushButton(self.frame)
        self.YesButton.setObjectName("YesButton")
        self.gridLayout.addWidget(self.YesButton, 2, 0, 1, 1)
        self.NoButton = QtWidgets.QPushButton(self.frame)
        self.NoButton.setObjectName("NoButton")
        self.gridLayout.addWidget(self.NoButton, 3, 0, 1, 1)
        self.message = QtWidgets.QPlainTextEdit(self.frame)
        self.message.setEnabled(False)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Message"))
        self.OkButton.setText(_translate("Form", "OK"))
        self.YesButton.setText(_translate("Form", "Yes"))
        self.NoButton.setText(_translate("Form", "No"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())