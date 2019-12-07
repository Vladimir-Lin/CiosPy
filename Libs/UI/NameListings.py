import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import pyttsx3
from   playsound                      import playsound
import urllib
import urllib . parse
from   pathlib                        import Path
import win32com . client
import mysql    . connector
from   mysql    . connector           import Error
import Actions
from   Actions                        import *
import CIOS
from   CIOS  . SQL                    import SqlQuery
from   CIOS  . SQL                    import SqlConnection
from   CIOS  . Database               import Tables
from   CIOS  . Voice     . Recognizer import Recognizer
from   CIOS  . Voice     . Audio      import AudioPlayer
from   CIOS  . Documents . JSON       import Load  as LoadJSON
from   CIOS  . Documents . JSON       import Merge as MergeJSON
from   CIOS  . Documents . Commands   import CommandsMapper
from   PyQt5                          import QtWidgets , QtGui , QtCore
from   PyQt5 . QtCore                 import QObject , pyqtSignal , Qt
from   PyQt5 . QtCore                 import QPoint , QPointF
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QTreeWidget , QTreeWidgetItem

##############################################################################

class NameListings ( QTreeWidget ) :

  emitRefresh = pyqtSignal ( )

  def __init__ ( self , parent = None ) :
    super ( NameListings , self ) . __init__ ( parent )
    ##########################################################################
    self . insertAction = QShortcut ( QKeySequence ( Qt.Key_Insert ) , self  )
    self . deleteAction = QShortcut ( QKeySequence ( Qt.Key_Delete ) , self  )
    self . insertAction . activated . connect ( self . Insert                )
    self . deleteAction . activated . connect ( self . Delete                )
    self . emitRefresh              . connect ( self . Refresh               )
    ##########################################################################
    self . Uuid       = 0
    self . Locality   = 1002
    self . Database   = ""
    self . Table      = ""
    self . Localities = { }
    self . Relevance  = { }
    self . Listings   = [ ]
    self . Configure    ( )
    ##########################################################################

  def Configure ( self ) :
    Labels = [ "語言" , "用途" , "名稱" , "次序" , "狀態" , "" ]
    self . setAttribute                 ( Qt   . WA_InputMethodEnabled )
    self . setDragDropMode              ( self . DragDrop              )
    self . setRootIsDecorated           ( False                        )
    self . setAlternatingRowColors      ( True                         )
    self . setHorizontalScrollBarPolicy ( Qt   . ScrollBarAsNeeded     )
    self . setVerticalScrollBarPolicy   ( Qt   . ScrollBarAsNeeded     )
    self . setColumnCount               ( 6                            )
    self . setHeaderLabels              ( Labels                       )
    self . itemDoubleClicked . connect  ( self . doubleClicked         )

  def focusInEvent ( self , event ) :
    print ( "Focus In" )
    super ( QTreeWidget , self ) . focusInEvent ( event )

  def focusOutEvent ( self , event ) :
    print ( "Focus Out" )
    super ( QTreeWidget , self ) . focusOutEvent ( event )

  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
    super ( QTreeWidget , self ) . contextMenuEvent ( event )

  def setUuid ( self , uuid ) :
    self . Uuid = uuid

  def setDatabase ( self , database ) :
    self . Database = database

  def setTable ( self , table ) :
    self . Table = table

  def setLocality ( self , locality ) :
    self . Locality = locality

  def startup ( self ) :
    threading . Thread ( target = self . loading ) . start ( )

  def TheName ( self , SC , Table , Uuid ) :
    LCY   = self . Locality
    DBS   = self . Database
    QQ    = f"select `name` from `{DBS}`.`{Table}` where ( `uuid` = {Uuid} ) and ( `locality` = {LCY} ) and ( `relevance` = 0 ) order by `priority` asc limit 0,1 ;"
    SC    . Query         ( QQ )
    NAMEX = SC . FetchOne (    )
    if ( not NAMEX ) :
      return ""
    if ( NAMEX == None ) :
      return ""
    if ( NAMEX is None ) :
      return ""
    if ( len ( NAMEX ) > 0 ) :
      return NAMEX [ 0 ]
    return ""

  def LoadRelevance  ( self , SC ) :
    self  . Relevance  = { }
    DBS    = self . Database
    QQ     = f"select `id`,`uuid`,`name` from `{DBS}`.`relevance` where `used` = 1 order by `id` asc ;"
    SC     . Query         ( QQ )
    LISTs  = SC . FetchAll (    )
    if ( not LISTs ) :
      return False
    for x in LISTs :
      Id = x [ 0 ]
      self . Relevance [ Id ] = x [ 2 ]
      N    = self . TheName ( SC , "names_languages" , x [ 1 ] )
      if ( len ( N ) > 0 ) :
        self . Relevance [ Id ] = N
    return True

  def LoadLocalities ( self , SC ) :
    self . Localities = { }
    DBS   = self . Database
    QQ    = f"select `uuid`,`code` from `{DBS}`.`locality` order by `code` asc ;"
    SC    . Query         ( QQ )
    LISTs = SC . FetchAll (    )
    if ( not LISTs ) :
      return False
    for x in LISTs :
      Id    = x [ 1 ]
      U     = x [ 0 ]
      N     = self . TheName ( SC , "names_languages" , U )
      if ( len ( N ) > 0 ) :
        self . Localities [ Id ] = N
    return True

  def LoadListings ( self , SC ) :
    self  . Listings = [ ]
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    QQ    = f"select `id`,`locality`,`priority`,`relevance`,`flags`,`name` from `{DBS}`.`{TBS}` where ( `uuid` = {UID} ) order by `locality` asc , `relevance` asc , `priority` asc ;"
    SC    . Query         ( QQ )
    self  . Listings = SC . FetchAll ( )
    return True

  def loading ( self ) :
    ##########################################################################
    SC = SqlConnection        (        )
    SC . ConnectTo            ( CiosDB )
    if not SC . isConnected   (        ) :
      return False
    ##########################################################################
    SC   . Prepare            (        )
    ##########################################################################
    self . LoadRelevance      ( SC     )
    self . LoadLocalities     ( SC     )
    self . LoadListings       ( SC     )
    ##########################################################################
    SC   . Close              (        )
    self . emitRefresh . emit (        )
    ##########################################################################
    return True

  def Refresh ( self )                                                       :
    ##########################################################################
    for x in self  . Listings                                                :
      ########################################################################
      it   = QTreeWidgetItem  ( [ self . Localities   [ int ( x [ 1 ] ) ]    ,
                                  self . Relevance    [ int ( x [ 3 ] ) ]    ,
                                                        str ( x [ 5 ] )      ,
                                                        str ( x [ 2 ] )      ,
                                                        str ( x [ 4 ] )      ,
                                                        ""                 ] )
      ########################################################################
      it   . setData          ( 0 , Qt . UserRole , int ( x [ 1 ] )          )
      it   . setData          ( 1 , Qt . UserRole , int ( x [ 3 ] )          )
      it   . setData          ( 2 , Qt . UserRole , str ( x [ 5 ] )          )
      it   . setData          ( 3 , Qt . UserRole , int ( x [ 2 ] )          )
      it   . setData          ( 4 , Qt . UserRole , str ( x [ 4 ] )          )
      it   . setData          ( 5 , Qt . UserRole , str ( x [ 0 ] )          )
      ########################################################################
      it   . setTextAlignment ( 3 , Qt . AlignRight                          )
      it   . setTextAlignment ( 4 , Qt . AlignRight                          )
      ########################################################################
      self . addTopLevelItem  ( it                                           )
    ##########################################################################
    for v in range ( 0 , 6 ) :
      self . resizeColumnToContents ( v )
    ##########################################################################
    return True

  def doubleClicked ( self , item , column ) :
    print ( column )
    return True

  def Insert ( self ) :
    print ( "Insert" )
    return True

  def Delete ( self ) :
    print ( "Delete" )
    return True

  def Menu ( self , pos ) :
    item  = self    . itemAt ( pos )
    atPos = QCursor . pos    (     )
    print ( pos , atPos )
    print ( item )
    return True

##############################################################################

if __name__ == '__main__':
  ############################################################################
  Uuid     = "0"
  Width    = 560
  Height   = 800
  Locality = 1002
  Title    = ""
  Table    = ""
  Database = "cios"
  ############################################################################
  argv = sys . argv [ 1: ]
  ############################################################################
  try                                                                        :
    opts, args = getopt . getopt                                             (
                   argv                                                      ,
                   "u:w:h:l:d:c:t:"                                          ,
                   [ "uuid="                                                 ,
                     "width="                                                ,
                     "height="                                               ,
                     "locality="                                             ,
                     "database="                                             ,
                     "caption="                                              ,
                     "title="                                              ] )
  except getopt . GetoptError                                                :
    sys . exit ( 1 )
  ############################################################################
  for opt, arg in opts                                                       :
    if   opt in ( "-u" , "--uuid"     )                                      :
      Uuid     = arg
    elif opt in ( "-w" , "--width"    )                                      :
      Width    = int ( arg )
    elif opt in ( "-h" , "--height"   )                                      :
      Height   = int ( arg )
    elif opt in ( "-l" , "--locality" )                                      :
      Locality = arg
    elif opt in ( "-d" , "--database" )                                      :
      Database = arg
    elif opt in ( "-c" , "--caption"  )                                      :
      Title    = arg
    elif opt in ( "-t" , "--table"    )                                      :
      Table    = arg
  ############################################################################
  if                      ( len ( Uuid  ) <  19                            ) :
    sys  . exit           ( 0                                                )
  if                      ( len ( Table ) <=  0                            ) :
    sys  . exit           ( 0                                                )
  ############################################################################
  app    = QApplication   ( sys . argv                                       )
  w      = NameListings   (                                                  )
  w      . setWindowTitle ( Title                                            )
  w      . resize         ( Width , Height                                   )
  w      . show           (                                                  )
  w      . setUuid        ( Uuid                                             )
  w      . setDatabase    ( Database                                         )
  w      . setTable       ( Table                                            )
  w      . setLocality    ( Locality                                         )
  w      . startup        (                                                  )
  sys    . exit           ( app . exec_ ( )                                  )
  ############################################################################
