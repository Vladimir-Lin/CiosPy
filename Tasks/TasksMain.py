# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TasksMain.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TasksMain(object):
    def setupUi(self, TasksMain):
        TasksMain.setObjectName("TasksMain")
        TasksMain.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/catalog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TasksMain.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(TasksMain)
        self.centralwidget.setObjectName("centralwidget")
        TasksMain.setCentralWidget(self.centralwidget)
        self.Menu = QtWidgets.QMenuBar(TasksMain)
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
        TasksMain.setMenuBar(self.Menu)
        self.Status = QtWidgets.QStatusBar(TasksMain)
        self.Status.setObjectName("Status")
        TasksMain.setStatusBar(self.Status)
        self.Tools = QtWidgets.QToolBar(TasksMain)
        self.Tools.setObjectName("Tools")
        TasksMain.addToolBar(QtCore.Qt.TopToolBarArea, self.Tools)
        self.actionQuit = QtWidgets.QAction(TasksMain)
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

        self.retranslateUi(TasksMain)
        self.actionQuit.triggered.connect(TasksMain.Quit)
        QtCore.QMetaObject.connectSlotsByName(TasksMain)

    def retranslateUi(self, TasksMain):
        _translate = QtCore.QCoreApplication.translate
        TasksMain.setWindowTitle(_translate("TasksMain", "Tasks Manager"))
        self.menuFile.setTitle(_translate("TasksMain", "File"))
        self.menuEdit.setTitle(_translate("TasksMain", "Edit"))
        self.menuHelp.setTitle(_translate("TasksMain", "Help"))
        self.menuWindows.setTitle(_translate("TasksMain", "Windows"))
        self.menuTools.setTitle(_translate("TasksMain", "Tools"))
        self.Tools.setWindowTitle(_translate("TasksMain", "toolBar"))
        self.actionQuit.setText(_translate("TasksMain", "Quit"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TasksMain = QtWidgets.QMainWindow()
    ui = Ui_TasksMain()
    ui.setupUi(TasksMain)
    TasksMain.show()
    sys.exit(app.exec_())
