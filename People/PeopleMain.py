# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PeopleMain.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PeopleMain(object):
    def setupUi(self, PeopleMain):
        PeopleMain.setObjectName("PeopleMain")
        PeopleMain.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/crowd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PeopleMain.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(PeopleMain)
        self.centralwidget.setObjectName("centralwidget")
        PeopleMain.setCentralWidget(self.centralwidget)
        self.Menu = QtWidgets.QMenuBar(PeopleMain)
        self.Menu.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.Menu.setObjectName("Menu")
        self.menuFile = QtWidgets.QMenu(self.Menu)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.Menu)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.Menu)
        self.menuHelp.setObjectName("menuHelp")
        self.menuWindows = QtWidgets.QMenu(self.Menu)
        self.menuWindows.setObjectName("menuWindows")
        self.menuTools = QtWidgets.QMenu(self.Menu)
        self.menuTools.setObjectName("menuTools")
        PeopleMain.setMenuBar(self.Menu)
        self.Status = QtWidgets.QStatusBar(PeopleMain)
        self.Status.setObjectName("Status")
        PeopleMain.setStatusBar(self.Status)
        self.Tools = QtWidgets.QToolBar(PeopleMain)
        self.Tools.setObjectName("Tools")
        PeopleMain.addToolBar(QtCore.Qt.TopToolBarArea, self.Tools)
        self.actionQuit = QtWidgets.QAction(PeopleMain)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon1)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.Menu.addAction(self.menuFile.menuAction())
        self.Menu.addAction(self.menuEdit.menuAction())
        self.Menu.addAction(self.menuTools.menuAction())
        self.Menu.addAction(self.menuWindows.menuAction())
        self.Menu.addAction(self.menuHelp.menuAction())
        self.Tools.addAction(self.actionQuit)

        self.retranslateUi(PeopleMain)
        self.actionQuit.triggered.connect(PeopleMain.Quit)
        QtCore.QMetaObject.connectSlotsByName(PeopleMain)

    def retranslateUi(self, PeopleMain):
        _translate = QtCore.QCoreApplication.translate
        PeopleMain.setWindowTitle(_translate("PeopleMain", "People"))
        self.menuFile.setTitle(_translate("PeopleMain", "File"))
        self.menuEdit.setTitle(_translate("PeopleMain", "Edit"))
        self.menuHelp.setTitle(_translate("PeopleMain", "Help"))
        self.menuWindows.setTitle(_translate("PeopleMain", "Windows"))
        self.menuTools.setTitle(_translate("PeopleMain", "Tools"))
        self.Tools.setWindowTitle(_translate("PeopleMain", "toolBar"))
        self.actionQuit.setText(_translate("PeopleMain", "Quit"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PeopleMain = QtWidgets.QMainWindow()
    ui = Ui_PeopleMain()
    ui.setupUi(PeopleMain)
    PeopleMain.show()
    sys.exit(app.exec_())
