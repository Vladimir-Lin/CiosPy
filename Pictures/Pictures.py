import os
import sys
sys . path . append ( os . path . dirname ( os . path . abspath (__file__) ) + "/../Libs" )
##############################################################################
import getopt
import time
import requests
import threading
import gettext
import json
import pyttsx3
from   playsound import playsound
##############################################################################
import urllib
import urllib . parse
##############################################################################
from   pathlib import Path
##############################################################################
import win32com . client
##############################################################################
import mysql    . connector
from   mysql    . connector import Error
##############################################################################
import Actions
##############################################################################
import CIOS
from   CIOS  . Voice     . Recognizer import Recognizer
from   CIOS  . Voice     . Audio      import AudioPlayer
from   CIOS  . Documents . JSON       import Load  as LoadJSON
from   CIOS  . Documents . JSON       import Merge as MergeJSON
from   CIOS  . Documents . Commands   import CommandsMapper
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QSystemTrayIcon
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QTextEdit
from   PyQt5 . QtWidgets              import QPlainTextEdit
from   PyQt5 . QtWidgets              import QMdiArea
from   PyQt5 . QtWidgets              import QStackedWidget
##############################################################################
from   CIOS  . Qt . VirtualGui        import VirtualGui
from   CIOS  . Qt . MenuManager       import MenuManager
from   CIOS  . Qt . TreeWidget        import TreeWidget
from   CIOS  . Qt . MainWindow        import MainWindow
##############################################################################
from   PeopleMain        import Ui_PeopleMain
import Resources
from   CrowdListings     import CrowdListings
##############################################################################

SysMenu     = None
KeepRunning = True
TurnOn      = True
Language    = "en-US"
Settings    = { }
UserConf    = { }
HomePath    = ""

##############################################################################

class PeopleWindow              ( MainWindow                               ) :

  def __init__                  ( self , parent = None                     ) :
    super                       ( MainWindow , self ) .  __init__ ( parent   )
    ##########################################################################
    self . ui = Ui_PeopleMain   (                                            )
    self . ui . setupUi         ( self                                       )
    self . Configure            (                                            )
    ##########################################################################
    return

  def Configure                 ( self                                     ) :
    ##########################################################################
    super                       ( ) . Configure (                            )
    ##########################################################################
    fnt  = self . font          (                                            )
    fnt  . setPixelSize         ( 16                                         )
    ##########################################################################
    self           . setFont    ( fnt                                        )
    self . stacked . setFont    ( fnt                                        )
    self . mdi     . setFont    ( fnt                                        )
    ##########################################################################
    return

  def Quit                      ( self                                     ) :
    self . hide                 (                                            )
    qApp . quit                 (                                            )
    return

  def startup ( self ) :
    return

  def Meridians                 ( self                                     ) :
    print ( "Meridians" )
    return

  def Acupunctures              ( self                                     ) :
    print ( "Acupunctures" )
    return

  def CrowdListings             ( self                                     ) :
    cl   = CrowdListings        ( self . mdi )
    self . addMdi               ( cl )
    cl   . setWindowTitle       ( "人物列表" )
    cl   . show ( )
    return

  def CrowdViews                ( self                                     ) :
    print ( "CrowdViews" )
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
  return True

def main                     (                                             ) :
  LoadOptions                (                                               )
  app   = QApplication       ( sys . argv                                    )
  tasks = PeopleWindow       (                                               )
  tasks . showMaximized      (                                               )
  tasks . startup            (                                               )
  sys   . exit               ( app . exec_ ( )                               )

if __name__ == '__main__' :
  main                       (                                               )
