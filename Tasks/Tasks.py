import os
import sys
sys . path . append ( os . path . dirname ( os . path . abspath (__file__) ) + "/../Libs" )
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
from   PyQt5 . QtWidgets import QMdiArea
from   PyQt5 . QtWidgets import QStackedWidget
from   TasksMain         import Ui_TasksMain
import TasksResources

SysMenu     = None
KeepRunning = True
TurnOn      = True
Language    = "en-US"
Settings    = { }
UserConf    = { }
HomePath    = ""

class TasksWindow            ( QtWidgets . QMainWindow ) :

  def __init__               ( self , parent = None    ) :
    super                    ( TasksWindow , self      ) . __init__ ( )
    self . ui = Ui_TasksMain (                         )
    self . ui . setupUi      ( self                    )
    self . Default           (                         )
    return

  def Default                       ( self                    ) :
    self . stacked = QStackedWidget ( self                    )
    self . mdi     = QMdiArea       ( self . stacked          )
    self . stacked . addWidget      ( self . mdi              )
    self . setCentralWidget         ( self . stacked          )
    return

  def Quit                   ( self                    ) :
    self . hide              (                         )
    qApp . quit              (                         )
    return

def LoadOptions              (                                             ) :
  global HomePath
  global Language
  global Settings
  HomePath  = str            ( Path . home ( )                               )
  STX       = LoadJSON       ( f"{HomePath}/CIOS/settings.json"              )
  UserConf  = LoadJSON       ( f"{HomePath}/CIOS/user.json"                  )
  STX       = MergeJSON      ( STX , UserConf                                )
  TaskConf  = LoadJSON       ( f"{HomePath}/CIOS/tasks.json"                 )
  Settings  = MergeJSON      ( STX , TaskConf                                )
  Language  = Settings [ "Voice" ] [ "Language" ]
  print ( Settings )
  return True

def main                     (                                             ) :
  LoadOptions                (                                               )
  app   = QApplication       ( sys . argv                                    )
  tasks = TasksWindow        (                                               )
  tasks . showMaximized      (                                               )
  sys   . exit               ( app . exec_ ( )                               )

if __name__ == '__main__' :
  main                       (                                               )
