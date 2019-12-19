import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import pyttsx3
from   playsound import playsound
import urllib
import urllib . parse
from   pathlib import Path
import win32com . client
import mysql    . connector
from   mysql    . connector import Error
import Actions
import CIOS
from   CIOS  . Voice     . Recognizer import Recognizer
from   CIOS  . Voice     . Audio      import AudioPlayer
from   CIOS  . Documents . JSON       import Load  as LoadJSON
from   CIOS  . Documents . JSON       import Merge as MergeJSON
from   CIOS  . Documents . Commands   import CommandsMapper
from   PyQt5             import QtWidgets , QtGui , QtCore
from   PyQt5 . QtCore    import QObject , pyqtSignal
from   PyQt5 . QtGui     import QIcon
from   PyQt5 . QtGui     import QCursor
from   PyQt5 . QtWidgets import QApplication
from   PyQt5 . QtWidgets import QWidget
from   PyQt5 . QtWidgets import qApp
from   PyQt5 . QtWidgets import QSystemTrayIcon
from   PyQt5 . QtWidgets import QMenu
from   PyQt5 . QtWidgets import QAction
from   PyQt5 . QtWidgets import QTextEdit
from   PyQt5 . QtWidgets import QPlainTextEdit
from   TasksMain         import Ui_TasksMain
import TasksResources

class TasksWindow            ( QtWidgets . QMainWindow ) :

  def __init__               ( self , parent = None    ) :
    super                    ( TasksWindow , self      ) . __init__ ( )
    self . ui = Ui_TasksMain (                         )
    self . ui . setupUi      ( self                    )
    return

  def Quit                   ( self                    ) :
    self . hide              (                         )
    qApp . quit              (                         )
    return

def main                     (                                             ) :
  app   = QApplication       ( sys . argv                                  )
  tasks = TasksWindow        (                                             )
  tasks . showMaximized      (                                             )
  sys   . exit               ( app . exec_ ( )                             )

if __name__ == '__main__' :
  main                       (                                             )
