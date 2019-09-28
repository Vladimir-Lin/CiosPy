import os
import sys
import getopt
import time
import requests
import threading
import mysql.connector
from mysql.connector import Error
import Actions
import CIOS

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui

class SystemTrayIcon ( QSystemTrayIcon ) :

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = menu.addAction("離開")
        exitAction . triggered . connect ( self . Quit )
        self.setContextMenu(menu)

    def Quit ( self ) :
      self . hide ( ) ;
      qApp . quit ( ) ;


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("D:/CIOS/CiosPy/images/64x64/Menu.png"), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
