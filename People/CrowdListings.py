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
from   CIOS  . Database               import Tables
from   CIOS  . Database               import TablePlans
from   CIOS  . Database               import Templates
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

class CrowdListings ( TreeWidget ) :

  ############################################################################

  ColumnName      = 0
  ColumnLanguage  = 1
  ColumnRelevance = 2
  ColumnPriority  = 3
  ColumnFlags     = 4
  ColumnId        = 5
  ColumnEmpty     = 6

  ############################################################################

  emitRefresh       = pyqtSignal ( )
  emitItemFlags     = pyqtSignal ( QTreeWidgetItem , str )
  emitNewItem       = pyqtSignal ( str , str , str , str , str )
  emitItemProerties = pyqtSignal ( QTreeWidgetItem , str , str , str )

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QTreeWidget , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################

    ##########################################################################

  ############################################################################

  def Configure ( self ) :
    return

  ############################################################################

  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusInEvent ( event )
    return

  ############################################################################

  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusOutEvent ( event )
    return

  ############################################################################

  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
    super ( QTreeWidget , self ) . contextMenuEvent ( event )
    return

  ############################################################################

  def startup ( self ) :
    self . clear ( )
    threading . Thread ( target = self . loading ) . start ( )
    return True

  ############################################################################

  def FocusIn ( self ) :
    return True

  ############################################################################

  def FocusOut ( self ) :
    return True

  ############################################################################

  def singleClicked ( self , item , column ) :
    return True

  ############################################################################

  def doubleClicked ( self , item , column ) :
    return True

  ############################################################################

  def Menu ( self , pos ) :
    ##########################################################################

    ##########################################################################
    return True

  ############################################################################

##############################################################################
