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
    self . insertAction = QShortcut ( QKeySequence ( Qt.Key_Insert ) , self  )
    self . deleteAction = QShortcut ( QKeySequence ( Qt.Key_Delete ) , self  )
    self . insertAction . activated . connect ( self . Insert                )
    self . deleteAction . activated . connect ( self . Delete                )
    self . emitRefresh              . connect ( self . Refresh               )
    self . emitItemFlags            . connect ( self . setItemFlags          )
    self . emitNewItem              . connect ( self . NewItem               )
    self . emitItemProerties        . connect ( self . UpdateItemProerties   )
    ##########################################################################
    self . Uuid        = 0
    self . Database    = ""
    self . Table       = ""
    self . RelevanceId = 0
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

  def toInt ( self , h ) :
    HEX = { "0" :  0 , "1" :  1 , "2" :  2 , "3" :  3 , "4" :  4             ,
            "5" :  5 , "6" :  6 , "7" :  7 , "8" :  8 , "9" :  9             ,
            "A" : 10 , "B" : 11 , "C" : 12 , "D" : 13 , "E" : 14 , "F" : 15  ,
            "a" : 10 , "b" : 11 , "c" : 12 , "d" : 13 , "e" : 14 , "f" : 15  }
    v   = 0
    s   = list ( h )
    if ( len ( s ) > 16 ) :
      return { "Correct" : False }
    for x in s :
      if ( x in HEX ) :
        k   = HEX [ x ]
        v   = v * 16
        v   = v + k
      else :
        return { "Correct" : False }
    if ( v >= 9223372036854775808 ) :
      return { "Correct" : False }
    return { "Correct" : True , "Value" : v }

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

  def setUuid ( self , uuid ) :
    self . Uuid = uuid
    return True

  ############################################################################

  def setDatabase ( self , database ) :
    self . Database = database
    return True

  ############################################################################

  def setTable ( self , table ) :
    self . Table = table
    return True

  ############################################################################

  def setItemFlags ( self , item , flags ) :
    HEX  = self . toInt ( flags )
    if ( not HEX [ "Correct" ] ) :
      return False
    item . setText ( self . ColumnFlags , flags )
    item . setData ( self . ColumnFlags , Qt . UserRole , HEX [ "Value" ] )
    return True

  ############################################################################

  def startup ( self ) :
    self . clear ( )
    threading . Thread ( target = self . loading ) . start ( )
    return True

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

  ############################################################################

  def AddNameItem ( self , Id , Locality , Relevance , Priority , Flags , Name ) :
    ##########################################################################
    it   = QTreeWidgetItem  ( [                       str ( Name      )      ,
                                self . Localities   [ int ( Locality  ) ]    ,
                                self . Relevance    [ int ( Relevance ) ]    ,
                                                      str ( Priority  )      ,
                                             self . toHex ( Flags     )      ,
                                                      str ( Id        )      ,
                                                      ""                   ] )
    ##########################################################################
    it   . setData          ( self . ColumnName      , Qt . UserRole , str ( Name      ) )
    it   . setData          ( self . ColumnLanguage  , Qt . UserRole , int ( Locality  ) )
    it   . setData          ( self . ColumnRelevance , Qt . UserRole , int ( Relevance ) )
    it   . setData          ( self . ColumnPriority  , Qt . UserRole , int ( Priority  ) )
    it   . setData          ( self . ColumnFlags     , Qt . UserRole , str ( Flags     ) )
    it   . setData          ( self . ColumnId        , Qt . UserRole , str ( Id        ) )
    ##########################################################################
    it   . setTextAlignment ( self . ColumnPriority , Qt . AlignRight        )
    it   . setTextAlignment ( self . ColumnFlags    , Qt . AlignRight        )
    it   . setTextAlignment ( self . ColumnId       , Qt . AlignRight        )
    ##########################################################################
    self . addTopLevelItem  ( it                                             )
    ##########################################################################
    return it

  ############################################################################

  def UpdateItemProerties ( self , Item , Locality , Relevance , Priority ) :
    ##########################################################################
    Item . setText ( self . ColumnLanguage  ,  self . Localities [ int ( Locality  ) ] )
    Item . setText ( self . ColumnRelevance ,  self . Relevance  [ int ( Relevance ) ] )
    Item . setText ( self . ColumnPriority  ,                      str ( Priority  )   )
    ##########################################################################
    Item . setData ( self . ColumnLanguage  , Qt . UserRole , int ( Locality  ) )
    Item . setData ( self . ColumnRelevance , Qt . UserRole , int ( Relevance ) )
    Item . setData ( self . ColumnPriority  , Qt . UserRole , int ( Priority  ) )
    ##########################################################################
    return True

  ############################################################################

  def Refresh ( self )                                                       :
    ##########################################################################
    for x in self  . Listings                                                :
      ########################################################################
      self . AddNameItem                                                     (
        str ( x [ 0 ] )                                                      ,
        str ( x [ 1 ] )                                                      ,
        str ( x [ 3 ] )                                                      ,
        str ( x [ 2 ] )                                                      ,
        str ( x [ 4 ] )                                                      ,
        str ( x [ 5 ] )                                                      )
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
      cb   . setMaxVisibleItems ( 15 )
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

  def UpdateName ( self , Item , Column , Id , Name ) :
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    SC    . LockWrites      ( [ Table ]       )
    ##########################################################################
    QQ    = f"update {Table} set `name` = %s where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC    . QueryValues     ( QQ , ( Name , ) )
    ##########################################################################
    QQ    = f"update {Table} set `length` = length(`name`) where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC    . Query           ( QQ )
    ##########################################################################
    SC    . UnlockTables    (                 )
    ##########################################################################
    SC    . Close           (           )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
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
    threading . Thread ( target = self . UpdateName , args = ( item , column , Id , Name , ) ) . start ( )
    return True

  ############################################################################

  def UpdateLanguage ( self , Item , Id , Language ) :
    ##########################################################################
    Relevance = Item . data  ( self . ColumnRelevance , Qt . UserRole )
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    Priority = -1
    QQ       = f"select `priority` from {Table} where ( `id` != {Id} ) and ( `uuid` = {UID} ) and ( `locality` = {Language} ) and ( `relevance` = {Relevance} ) order by `priority` desc limit 0,1 ;"
    SC       . Query         ( QQ )
    PRID     = SC . FetchOne (    )
    if not ( ( not PRID ) or ( PRID == None  ) or ( PRID is None ) ) :
      Priority = PRID [ 0 ]
    Priority = Priority + 1
    ##########################################################################
    QQ       = f"update {Table} set `locality` = {Language} , `priority` = {Priority} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC       . Query         ( QQ )
    ##########################################################################
    SC       . UnlockTables  (    )
    ##########################################################################
    SC       . Close         (    )
    ##########################################################################
    self . emitItemProerties . emit                                          (
      Item                                                                   ,
      str ( Language  )                                                      ,
      str ( Relevance )                                                      ,
      str ( Priority  )                                                      )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  def languageChanged ( self , Id ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item      = self   . CurrentItem [ "Item"   ]
    column    = self   . CurrentItem [ "Column" ]
    widget    = self   . CurrentItem [ "Widget" ]
    Language  = widget . itemData ( widget . currentIndex ( ) )
    self      . removeParked (          )
    oldLang   = item . data  ( column , Qt . UserRole )
    oldLang   = int          ( oldLang                )
    if ( Language == oldLang ) :
      return False
    Id        = item . data          ( 5      , Qt . UserRole )
    threading . Thread ( target = self . UpdateLanguage , args = ( item , Id , Language , ) ) . start ( )
    return True

  ############################################################################

  def UpdateRelevance ( self , Item , Id , Relevance ) :
    ##########################################################################
    Language = Item . data  ( self . ColumnLanguage , Qt . UserRole )
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    Priority = -1
    QQ       = f"select `priority` from {Table} where ( `id` != {Id} ) and ( `uuid` = {UID} ) and ( `locality` = {Language} ) and ( `relevance` = {Relevance} ) order by `priority` desc limit 0,1 ;"
    SC       . Query         ( QQ )
    PRID     = SC . FetchOne (    )
    if not ( ( not PRID ) or ( PRID == None  ) or ( PRID is None ) ) :
      Priority = PRID [ 0 ]
    Priority = Priority + 1
    ##########################################################################
    QQ       = f"update {Table} set `relevance` = {Relevance} , `priority` = {Priority} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC       . Query         ( QQ )
    ##########################################################################
    SC       . UnlockTables  (    )
    ##########################################################################
    SC       . Close         (    )
    ##########################################################################
    self . emitItemProerties . emit                                          (
      Item                                                                   ,
      str ( Language  )                                                      ,
      str ( Relevance )                                                      ,
      str ( Priority  )                                                      )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  def relevanceChanged ( self , Id ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item      = self   . CurrentItem [ "Item"   ]
    column    = self   . CurrentItem [ "Column" ]
    widget    = self   . CurrentItem [ "Widget" ]
    Relevance = widget . itemData ( widget . currentIndex ( ) )
    self   . removeParked         (          )
    oldRelev  = item . data  ( column , Qt . UserRole )
    oldRelev  = int          ( oldRelev               )
    if ( Relevance == oldRelev ) :
      return False
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateRelevance , args = ( item , Id , Relevance , ) ) . start ( )
    return True

  ############################################################################

  def UpdatePriority ( self , Item , Id , Priority ) :
    ##########################################################################
    Language  = Item . data  ( self . ColumnLanguage  , Qt . UserRole )
    Relevance = Item . data  ( self . ColumnRelevance , Qt . UserRole )
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    QQ       = f"select `id` from {Table} where ( `id` != {Id} ) and ( `uuid` = {UID} ) and ( `locality` = {Language} ) and ( `relevance` = {Relevance} ) and ( `priority` = {Priority} ) limit 0,1 ;"
    SC       . Query         ( QQ )
    PRID     = SC . FetchOne (    )
    if not ( ( not PRID ) or ( PRID == None  ) or ( PRID is None ) ) :
      Priority = -1
      QQ       = f"select `priority` from {Table} where ( `id` != {Id} ) and ( `uuid` = {UID} ) and ( `locality` = {Language} ) and ( `relevance` = {Relevance} ) order by `priority` desc limit 0,1 ;"
      SC       . Query         ( QQ )
      PRID     = SC . FetchOne (    )
      if not ( ( not PRID ) or ( PRID == None  ) or ( PRID is None ) ) :
        Priority = PRID [ 0 ]
      Priority = Priority + 1
    ##########################################################################
    QQ       = f"update {Table} set `priority` = {Priority} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC       . Query         ( QQ )
    ##########################################################################
    SC       . UnlockTables  (    )
    ##########################################################################
    SC       . Close         (    )
    ##########################################################################
    self . emitItemProerties . emit                                          (
      Item                                                                   ,
      str ( Language  )                                                      ,
      str ( Relevance )                                                      ,
      str ( Priority  )                                                      )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
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
    oldPriority = item . data  ( column , Qt . UserRole )
    oldPriority = int          ( oldPriority            )
    if ( Priority == oldPriority ) :
      return False
    Id     = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdatePriority , args = ( item , Id , Priority , ) ) . start ( )
    return True

  ############################################################################

  def UpdateFlags ( self , Item , Column , Id , Flags ) :
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    QQ    = f"update {Table} set `flags` = {Flags} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC    . LockWrites      ( [ Table ] )
    SC    . Query           ( QQ        )
    SC    . UnlockTables    (           )
    ##########################################################################
    SC    . Close           (           )
    ##########################################################################
    HEX   = self . toHex    ( Flags                 )
    self . emitItemFlags . emit ( Item , HEX )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  def flagsChanged ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item      = self   . CurrentItem [ "Item"   ]
    column    = self   . CurrentItem [ "Column" ]
    widget    = self   . CurrentItem [ "Widget" ]
    Flags     = widget . text        (          )
    OldFlags  = item   . data        ( column , Qt . UserRole )
    R         = self   . toInt       ( Flags    )
    self      . removeParked         (          )
    if ( not R [ "Correct" ] ) :
      return False
    V         = R [ "Value" ]
    if ( V == OldFlags ) :
      return False
    Id        = item . data          ( 5 , Qt . UserRole )
    threading . Thread ( target = self . UpdateFlags , args = ( item , column , Id , V , ) ) . start ( )
    return True

  ############################################################################

  def NewItem ( self , Id , Locality , Relevance , Priority , Flags )        :
    ##########################################################################
    it = self . AddNameItem                                                  (
           str ( Id        )                                                 ,
           str ( Locality  )                                                 ,
           str ( Relevance )                                                 ,
           str ( Priority  )                                                 ,
           str ( Flags     )                                                 ,
           ""                                                                )
    self . setCurrentItem ( it )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  ############################################################################

  def AppendItem ( self ) :
    ##########################################################################
    SC = SqlConnection       (        )
    SC . ConnectTo           ( CiosDB )
    if not SC . isConnected  (        ) :
      return False
    ##########################################################################
    SC    . Prepare          (        )
    ##########################################################################
    DBS      = self . Database
    TBS      = self . Table
    UID      = self . Uuid
    LCID     = self . Locality
    REVID    = self . RelevanceId
    Table    = f"`{DBS}`.`{TBS}`"
    ##########################################################################
    SC       . LockWrites    ( [ Table ] )
    ##########################################################################
    Priority = -1
    QQ       = f"select `priority` from {Table} where ( `uuid` = {UID} ) and ( `locality` = {LCID} ) and ( `relevance` = {REVID} ) order by `priority` desc limit 0,1 ;"
    SC       . Query         ( QQ )
    PRID     = SC . FetchOne (    )
    if not ( ( not PRID ) or ( PRID == None  ) or ( PRID is None ) ) :
      Priority = PRID [ 0 ]
    Priority = Priority + 1
    ##########################################################################
    QQ       = f"insert into {Table} ( `uuid`,`locality`,`priority`,`relevance`,`name` ) values ( {UID} , {LCID} , {Priority} , {REVID} , '' ) ;"
    SC       . Query         ( QQ )
    ##########################################################################
    QQ    = f"select `id`,`locality`,`priority`,`relevance`,`flags` from {Table} where ( `uuid` = {UID} ) and ( `locality` = {LCID} ) and ( `relevance` = {REVID} ) and ( `priority` = {Priority} ) limit 0,1 ;"
    SC    . Query         ( QQ )
    RC    = SC . FetchOne (    )
    ##########################################################################
    SC       . UnlockTables  (           )
    SC       . Close         (           )
    ##########################################################################
    if not ( ( not RC ) or ( RC == None  ) or ( RC is None ) ) :
      Id    = RC [ 0 ]
      Flags = RC [ 4 ]
    self . emitNewItem . emit                                                (
      str ( Id       )                                                       ,
      str ( LCID     )                                                       ,
      str ( REVID    )                                                       ,
      str ( Priority )                                                       ,
      str ( Flags    )                                                       )
    ##########################################################################
    return True

  ############################################################################

  def Insert ( self ) :
    threading . Thread ( target = self . AppendItem ) . start ( )
    return True

  ############################################################################

  def RemoveItem ( self , Id ) :
    ##########################################################################
    SC    = SqlConnection   (        )
    SC    . ConnectTo       ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    DBS   = self . Database
    TBS   = self . Table
    UID   = self . Uuid
    Table = f"`{DBS}`.`{TBS}`"
    ##########################################################################
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    QQ    = f"delete from {Table} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    SC    . Query           ( QQ        )
    ##########################################################################
    SC    . UnlockTables    (           )
    SC    . Close           (           )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/delete.mp3" )
    ##########################################################################
    return True

  ############################################################################

  def DeleteItem ( self , item ) :
    Id = item . data ( 5 , Qt . UserRole )
    idx = self . indexOfTopLevelItem ( item )
    if ( idx >= 0 ) :
      self . takeTopLevelItem ( idx )
      threading . Thread ( target = self . RemoveItem , args = ( Id , ) ) . start ( )
    return True

  ############################################################################

  def Delete ( self ) :
    ##########################################################################
    item = self . currentItem ( )
    if ( None == item ) :
      return False
    ##########################################################################
    return self . DeleteItem ( item )

  ############################################################################

  def Menu ( self , pos ) :
    id           = 0
    MenuMap      = { }
    item         = self    . itemAt ( pos )
    atPos        = QCursor . pos    (     )
    menu         = QMenu ( self )
    menu         . setFont ( self . font ( ) )
    reloadAction = menu  . addAction ( "重新載入" )
    MenuMap [ reloadAction ] = 1000
    ##########################################################################
    menu     . addSeparator ( )
    ##########################################################################
    appendAction = menu  . addAction ( "新增" )
    MenuMap [ appendAction ] = 1001
    ##########################################################################
    if ( None == item ) :
      pass
    else :
      deleteAction = menu  . addAction ( "刪除" )
      MenuMap [ deleteAction ] = 1002
      id = item . data ( 5 , Qt . UserRole )
    idShown  = not self . isColumnHidden ( 5 )
    menu     . addSeparator ( )
    ##########################################################################
    idAction = menu . addAction ( "排序" )
    idAction . setCheckable ( True )
    idAction . setChecked   ( self . isSortingEnabled ( ) )
    MenuMap [ idAction ] = 1003
    ##########################################################################
    idAction = menu . addAction ( "編號" )
    idAction . setCheckable ( True )
    idAction . setChecked   ( idShown )
    MenuMap [ idAction ] = 1004
    ##########################################################################
    menu     . addSeparator ( )
    ##########################################################################
    languageMenu  = menu . addMenu ( "內定語言" )
    languageMenu  . setFont ( self . font ( ) )
    KK  = self . Localities . keys ( )
    for x in KK :
      act = languageMenu . addAction ( self . Localities [ x ] )
      act . setCheckable ( True )
      MenuMap [ act ] = 1000000 + x
      if ( self . Locality == x ) :
        act . setChecked ( True )
    ##########################################################################
    relevanceMenu = menu . addMenu ( "內定用途" )
    relevanceMenu . setFont ( self . font ( ) )
    KK  = self . Relevance . keys ( )
    for x in KK :
      act = relevanceMenu . addAction ( self . Relevance [ x ] )
      act . setCheckable ( True )
      MenuMap [ act ] = 2000000 + x
      if ( self . RelevanceId == x ) :
        act . setChecked ( True )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/open.mp3" )
    action = menu . exec_ ( atPos )
    ##########################################################################
    if ( None == action ) :
      return False
    ##########################################################################
    MenuId = MenuMap [ action ]
    if   ( 1000 == MenuId ) :
      self . startup ( )
    if   ( 1001 == MenuId ) :
      self . Insert ( )
    elif ( 1002 == MenuId ) :
      self . DeleteItem ( item )
    elif ( 1003 == MenuId ) :
      idShown = action . isChecked ( )
      if ( idShown ) :
        self . setSortingEnabled ( True  )
      else :
        self . setSortingEnabled ( False )
    elif ( 1004 == MenuId ) :
      idShown = action . isChecked ( )
      if ( idShown ) :
        self . setColumnHidden ( 5 , False )
      else :
        self . setColumnHidden ( 5 , True  )
    elif ( MenuId > 1000000 ) and ( MenuId < 2000000 ) :
      self . Locality    = MenuId - 1000000
    elif ( MenuId > 2000000 ) and ( MenuId < 3000000 ) :
      self . RelevanceId = MenuId - 2000000
    ##########################################################################
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
