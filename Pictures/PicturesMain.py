# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PicturesMain.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PicturesMain(object):
    def setupUi(self, PicturesMain):
        PicturesMain.setObjectName("PicturesMain")
        PicturesMain.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/crowd.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PicturesMain.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(PicturesMain)
        self.centralwidget.setObjectName("centralwidget")
        PicturesMain.setCentralWidget(self.centralwidget)
        self.Menu = QtWidgets.QMenuBar(PicturesMain)
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
        self.menuPages = QtWidgets.QMenu(self.menuWindows)
        self.menuPages.setObjectName("menuPages")
        self.menuWindowLists = QtWidgets.QMenu(self.menuWindows)
        self.menuWindowLists.setObjectName("menuWindowLists")
        self.menuTools = QtWidgets.QMenu(self.Menu)
        self.menuTools.setObjectName("menuTools")
        self.menuViews = QtWidgets.QMenu(self.Menu)
        self.menuViews.setObjectName("menuViews")
        self.menuGalleries = QtWidgets.QMenu(self.Menu)
        self.menuGalleries.setObjectName("menuGalleries")
        PicturesMain.setMenuBar(self.Menu)
        self.Status = QtWidgets.QStatusBar(PicturesMain)
        self.Status.setObjectName("Status")
        PicturesMain.setStatusBar(self.Status)
        self.Tools = QtWidgets.QToolBar(PicturesMain)
        self.Tools.setObjectName("Tools")
        PicturesMain.addToolBar(QtCore.Qt.TopToolBarArea, self.Tools)
        self.actionQuit = QtWidgets.QAction(PicturesMain)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon1)
        self.actionQuit.setObjectName("actionQuit")
        self.actionMeridian = QtWidgets.QAction(PicturesMain)
        self.actionMeridian.setObjectName("actionMeridian")
        self.actionAcupunctures = QtWidgets.QAction(PicturesMain)
        self.actionAcupunctures.setObjectName("actionAcupunctures")
        self.actionCrowdListings = QtWidgets.QAction(PicturesMain)
        self.actionCrowdListings.setObjectName("actionCrowdListings")
        self.actionCrowdViews = QtWidgets.QAction(PicturesMain)
        self.actionCrowdViews.setObjectName("actionCrowdViews")
        self.actionTags = QtWidgets.QAction(PicturesMain)
        self.actionTags.setObjectName("actionTags")
        self.actionAll = QtWidgets.QAction(PicturesMain)
        self.actionAll.setObjectName("actionAll")
        self.menuFile.addAction(self.actionQuit)
        self.menuWindows.addAction(self.menuPages.menuAction())
        self.menuWindows.addAction(self.menuWindowLists.menuAction())
        self.menuTools.addAction(self.actionTags)
        self.menuViews.addAction(self.actionAll)
        self.Menu.addAction(self.menuFile.menuAction())
        self.Menu.addAction(self.menuEdit.menuAction())
        self.Menu.addAction(self.menuViews.menuAction())
        self.Menu.addAction(self.menuGalleries.menuAction())
        self.Menu.addAction(self.menuTools.menuAction())
        self.Menu.addAction(self.menuWindows.menuAction())
        self.Menu.addAction(self.menuHelp.menuAction())
        self.Tools.addAction(self.actionQuit)

        self.retranslateUi(PicturesMain)
        self.actionQuit.triggered.connect(PicturesMain.Quit)
        self.actionAll.triggered.connect(PicturesMain.AllPictures)
        QtCore.QMetaObject.connectSlotsByName(PicturesMain)

    def retranslateUi(self, PicturesMain):
        _translate = QtCore.QCoreApplication.translate
        PicturesMain.setWindowTitle(_translate("PicturesMain", "Pictures"))
        self.menuFile.setTitle(_translate("PicturesMain", "File"))
        self.menuEdit.setTitle(_translate("PicturesMain", "Edit"))
        self.menuHelp.setTitle(_translate("PicturesMain", "Help"))
        self.menuWindows.setTitle(_translate("PicturesMain", "Windows"))
        self.menuPages.setTitle(_translate("PicturesMain", "Pages"))
        self.menuWindowLists.setTitle(_translate("PicturesMain", "Window listings"))
        self.menuTools.setTitle(_translate("PicturesMain", "Tools"))
        self.menuViews.setTitle(_translate("PicturesMain", "Views"))
        self.menuGalleries.setTitle(_translate("PicturesMain", "Galleries"))
        self.Tools.setWindowTitle(_translate("PicturesMain", "toolBar"))
        self.actionQuit.setText(_translate("PicturesMain", "Quit"))
        self.actionMeridian.setText(_translate("PicturesMain", "Meridians"))
        self.actionAcupunctures.setText(_translate("PicturesMain", "Acupunctures"))
        self.actionCrowdListings.setText(_translate("PicturesMain", "Listings"))
        self.actionCrowdViews.setText(_translate("PicturesMain", "Views"))
        self.actionTags.setText(_translate("PicturesMain", "Tags"))
        self.actionAll.setText(_translate("PicturesMain", "All"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PicturesMain = QtWidgets.QMainWindow()
    ui = Ui_PicturesMain()
    ui.setupUi(PicturesMain)
    PicturesMain.show()
    sys.exit(app.exec_())
