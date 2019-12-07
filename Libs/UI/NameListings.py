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
from   CIOS  . Qt        . VirtualGui import VirtualGui
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QTreeWidget , QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox

##############################################################################

class NameListings ( QTreeWidget , VirtualGui ) :

  ############################################################################

  emitRefresh = pyqtSignal ( )

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QTreeWidget , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    self . insertAction = QShortcut ( QKeySequence ( Qt.Key_Insert ) , self  )
    self . deleteAction = QShortcut ( QKeySequence ( Qt.Key_Delete ) , self  )
    self . insertAction . activated . connect ( self . Insert                )
    self . deleteAction . activated . connect ( self . Delete                )
    self . emitRefresh              . connect ( self . Refresh               )
    ##########################################################################
    self . Uuid        = 0
    self . Locality    = 1002
    self . Database    = ""
    self . Table       = ""
    self . Player      = AudioPlayer ( )
    self . Localities  = { }
    self . Relevance   = { }
    self . Listings    = [ ]
    self . CurrentItem = { }
    self . Configure     ( )
    ##########################################################################

  ############################################################################

  def Configure ( self ) :
    Labels = [ "名稱" , "語言" , "用途" , "次序" , "狀態" , "編號" , "" ]
    fnt    = self . font                  (                              )
    fnt    . setPixelSize                 ( 20                           )
    self   . setFont                      ( fnt                          )
    self   . setAttribute                 ( Qt   . WA_InputMethodEnabled )
    self   . setDragDropMode              ( self . DragDrop              )
    self   . setRootIsDecorated           ( False                        )
    self   . setAlternatingRowColors      ( True                         )
    self   . setHorizontalScrollBarPolicy ( Qt   . ScrollBarAsNeeded     )
    self   . setVerticalScrollBarPolicy   ( Qt   . ScrollBarAsNeeded     )
    self   . setSelectionMode             ( self . SingleSelection       )
    self   . setColumnCount               ( 7                            )
    self   . setColumnHidden              ( 5    , True                  )
    self   . setColumnWidth               ( 6    , 5                     )
    self   . setHeaderLabels              ( Labels                       )
    self   . itemDoubleClicked . connect  ( self . doubleClicked         )
    self   . itemClicked       . connect  ( self . singleClicked         )

  ############################################################################

  def toHex ( self , v ) :
    HEX = {  0 : "0" ,  1 : "1" ,  2 : "2" ,  3 : "3"                        ,
             4 : "4" ,  5 : "5" ,  6 : "6" ,  7 : "7"                        ,
             8 : "8" ,  9 : "9" , 10 : "A" , 11 : "B"                        ,
            12 : "C" , 13 : "D" , 14 : "E" , 15 : "F"                        }
    SS  = ""
    VV  = int ( v )
    for i in range ( 0 , 16 ) :
      DD = int ( VV % 16 )
      VV = int ( VV / 16 )
      WW = HEX [ DD      ]
      SS = f"{WW}{SS}"
    return SS

  ############################################################################

  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusInEvent ( event )

  ############################################################################

  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QTreeWidget , self ) . focusOutEvent ( event )

  ############################################################################

  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
    super ( QTreeWidget , self ) . contextMenuEvent ( event )

  ############################################################################

  def setUuid ( self , uuid ) :
    self . Uuid = uuid

  ############################################################################

  def setDatabase ( self , database ) :
    self . Database = database

  ############################################################################

  def setTable ( self , table ) :
    self . Table = table

  ############################################################################

  def setLocality ( self , locality ) :
    self . Locality = locality

  ############################################################################

  def startup ( self ) :
    threading . Thread ( target = self . loading ) . start ( )

  ############################################################################

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

  ############################################################################

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

  ############################################################################

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

  ############################################################################

  def LoadListings ( self , SC ) :
    self  . Listings = [ ]
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    QQ    = f"select `id`,`locality`,`priority`,`relevance`,`flags`,`name` from `{DBS}`.`{TBS}` where ( `uuid` = {UID} ) order by `locality` asc , `relevance` asc , `priority` asc ;"
    SC    . Query         ( QQ )
    self  . Listings = SC . FetchAll ( )
    return True

  ############################################################################

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
      it   = QTreeWidgetItem  ( [                       str ( x [ 5 ] )      ,
                                  self . Localities   [ int ( x [ 1 ] ) ]    ,
                                  self . Relevance    [ int ( x [ 3 ] ) ]    ,
                                                        str ( x [ 2 ] )      ,
                                               self . toHex ( x [ 4 ] )      ,
                                                        str ( x [ 0 ] )      ,
                                                        ""                 ] )
      ########################################################################
      it   . setData          ( 0 , Qt . UserRole , str ( x [ 5 ] )          )
      it   . setData          ( 1 , Qt . UserRole , int ( x [ 1 ] )          )
      it   . setData          ( 2 , Qt . UserRole , int ( x [ 3 ] )          )
      it   . setData          ( 3 , Qt . UserRole , int ( x [ 2 ] )          )
      it   . setData          ( 4 , Qt . UserRole , str ( x [ 4 ] )          )
      it   . setData          ( 5 , Qt . UserRole , str ( x [ 0 ] )          )
      ########################################################################
      it   . setTextAlignment ( 3 , Qt . AlignRight                          )
      it   . setTextAlignment ( 4 , Qt . AlignRight                          )
      it   . setTextAlignment ( 5 , Qt . AlignRight                          )
      ########################################################################
      self . addTopLevelItem  ( it                                           )
    ##########################################################################
    for v in range ( 0 , 6 ) :
      self . resizeColumnToContents ( v )
    ##########################################################################
    return True

  ############################################################################

  def FocusIn ( self ) :
    return True

  ############################################################################

  def FocusOut ( self ) :
    return True

  ############################################################################

  def removeParked ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self . CurrentItem [ "Item"   ]
    column = self . CurrentItem [ "Column" ]
    self   . removeItemWidget ( item , column )
    self   . CurrentItem = { }
    return True

  ############################################################################

  def GetLanguageLists ( self , Id ) :
    cb  = QComboBox ( self )
    KK  = self . Localities . keys ( )
    idx = 0
    cnt = -1
    for x in KK :
      cb . addItem ( self . Localities [ x ] , x )
      if ( Id == x ) :
        cnt = idx
      idx = idx + 1
    if ( cnt >= 0 ) :
      cb . setCurrentIndex ( cnt )
    return cb

  ############################################################################

  def GetRelevanceLists ( self , Id ) :
    cb  = QComboBox ( self )
    KK  = self . Relevance . keys ( )
    idx = 0
    cnt = -1
    for x in KK :
      cb . addItem ( self . Relevance [ x ] , x )
      if ( Id == x ) :
        cnt = idx
      idx = idx + 1
    if ( cnt >= 0 ) :
      cb . setCurrentIndex ( cnt )
    return cb

  ############################################################################

  def singleClicked ( self , item , column ) :
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/click.mp3" )
    return True

  ############################################################################

  def doubleClicked ( self , item , column ) :
    ##########################################################################
    self   . removeParked ( )
    ##########################################################################
    if   ( 0 == column ) :
      ########################################################################
      le   = QLineEdit       ( self                   )
      le   . setText         ( item . text ( column ) )
      le   . editingFinished . connect ( self . nameChanged )
      self . setItemWidget ( item , column , le )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = le
      ########################################################################
    elif ( 1 == column ) :
      ########################################################################
      Id   = item . data             ( 1 , Qt . UserRole      )
      cb   = self . GetLanguageLists ( Id                     )
      cb   . activated . connect     ( self . languageChanged )
      self . setItemWidget ( item , column , cb )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = cb
      cb   . showPopup ( )
      ########################################################################
    elif ( 2 == column ) :
      ########################################################################
      Id   = item . data              ( 2 , Qt . UserRole       )
      cb   = self . GetRelevanceLists ( Id                      )
      cb   . activated . connect      ( self . relevanceChanged )
      self . setItemWidget ( item , column , cb )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = cb
      cb   . showPopup ( )
      ########################################################################
    elif ( 3 == column ) :
      ########################################################################
      val  = int ( item . data ( 3 , Qt . UserRole )  )
      sb   = QSpinBox        ( self                   )
      sb   . setMinimum      ( 0                      )
      sb   . setAlignment    ( Qt . AlignRight        )
      sb   . setValue        ( val                    )
      sb   . editingFinished . connect ( self . priorityChanged )
      self . setItemWidget ( item , column , sb )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = sb
      ########################################################################
    elif ( 4 == column ) :
      ########################################################################
      le   = QLineEdit       ( self                   )
      le   . setText         ( item . text ( column ) )
      le   . editingFinished . connect ( self . flagsChanged )
      self . setItemWidget ( item , column , le )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = le
      ########################################################################
    return True

  ############################################################################

  def UpdateName ( self , Item , Id , Name ) :
    print ( Id , Name )
    return True

  def nameChanged ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Name   = widget . text        (          )
    self   . removeParked         (          )
    item   . setText              ( 0 , Name )
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateName , args = ( item , Id , Name , ) ) . start ( )
    return True

  ############################################################################

  def UpdateLanguage ( self , Item , Id , Language ) :
    print ( Id , Language )
    return True

  def languageChanged ( self , Id ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Language = widget . itemData ( widget . currentIndex ( ) )
    self   . removeParked         (          )
    item   . setText              ( column , self . Localities [ Language ] )
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateLanguage , args = ( item , Id , Language , ) ) . start ( )
    return True

  ############################################################################

  def UpdateRelevance ( self , Item , Id , Relevance ) :
    print ( Id , Relevance )
    return True

  def relevanceChanged ( self , Id ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Relevance = widget . itemData ( widget . currentIndex ( ) )
    self   . removeParked         (          )
    item   . setText              ( column , self . Relevance [ Relevance ] )
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateRelevance , args = ( item , Id , Relevance , ) ) . start ( )
    return True

  ############################################################################

  def UpdatePriority ( self , Item , Id , Priority ) :
    print ( Id , Priority )
    return True

  def priorityChanged ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Priority = widget . value     (          )
    self   . removeParked         (          )
    item   . setText              ( column , str ( Priority ) )
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdatePriority , args = ( item , Id , Priority , ) ) . start ( )
    return True

  ############################################################################

  def UpdateFlags ( self , Item , Id , Flags ) :
    print ( Id , Flags )
    return True

  def flagsChanged ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Flags  = widget . text        (          )
    self   . removeParked         (          )
    item   . setText              ( column , Flags )
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateFlags , args = ( item , Id , Flags , ) ) . start ( )
    return True

  ############################################################################

  def AppendItem ( self ) :
    print ( "AppendItem" )
    return False

  ############################################################################

  def Insert ( self ) :
    threading . Thread ( target = self . AppendItem ) . start ( )
    return True

  ############################################################################

  def RemoveItem ( self , Id ) :
    UID = self . Uuid
    print ( "Remove" , UID , Id )
    return False

  ############################################################################

  def Delete ( self ) :
    ##########################################################################
    item = self . currentItem ( )
    if ( None == item ) :
      return False
    ##########################################################################
    Id = item . data ( 5 , Qt . UserRole )
    idx = self . indexOfTopLevelItem ( item )
    if ( idx >= 0 ) :
      self . takeTopLevelItem ( idx )
      threading . Thread ( target = self . RemoveItem , args = ( Id , ) ) . start ( )
    ##########################################################################
    return True

  ############################################################################

  def Menu ( self , pos ) :
    id           = 0
    MenuMap      = { }
    item         = self    . itemAt ( pos )
    atPos        = QCursor . pos    (     )
    menu         = QMenu ( self )
    menu         . setFont ( self . font ( ) )
    appendAction = menu  . addAction ( "新增" )
    MenuMap [ appendAction ] = 1001
    if ( None == item ) :
      pass
    else :
      deleteAction = menu  . addAction ( "刪除" )
      MenuMap [ deleteAction ] = 1002
      id = item . data ( 5 , Qt . UserRole )
      print ( id )
    idShown  = not self . isColumnHidden ( 5 )
    menu     . addSeparator ( )
    idAction = menu . addAction ( "編號" )
    idAction . setCheckable ( True )
    idAction . setChecked   ( idShown )
    MenuMap [ idAction ] = 1003
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/open.mp3" )
    action = menu . exec_ ( atPos )
    if ( None == action ) :
      return False
    MenuId = MenuMap [ action ]
    if   ( 1001 == MenuId ) :
      self . Insert ( )
    elif ( 1002 == MenuId ) :
      pass
    elif ( 1003 == MenuId ) :
      idShown = action . isChecked ( )
      if ( idShown ) :
        self . setColumnHidden ( 5 , False )
      else :
        self . setColumnHidden ( 5 , True  )
    print ( MenuId )
    return True

  ############################################################################

##############################################################################

if __name__ == '__main__':
  ############################################################################
  Uuid     = "0"
  Width    = 960
  Height   = 480
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
