# -*- coding: utf-8 -*-
##############################################################################
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
from   Actions                        import *
##############################################################################
import CIOS
from   CIOS  . SQL                    import SqlQuery
from   CIOS  . SQL                    import SqlConnection
##############################################################################
from   CIOS  . Voice     . Recognizer import Recognizer
from   CIOS  . Voice     . Audio      import AudioPlayer
##############################################################################
from   CIOS  . Documents . JSON       import Load  as LoadJSON
from   CIOS  . Documents . JSON       import Merge as MergeJSON
from   CIOS  . Documents . Commands   import CommandsMapper
##############################################################################
from   CIOS  . Database               import Tables
from   CIOS  . Database               import TablePlans
from   CIOS  . Database               import Templates
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QSystemTrayIcon
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
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

  ColumnName  = 0
  ColumnUsed  = 1
  ColumnFlags = 2
  ColumnUuid  = 3
  ColumnId    = 4
  ColumnEmpty = 5

  ############################################################################

  emitRefresh   = pyqtSignal (                                   )
  emitNewItem   = pyqtSignal ( str , str , str , str , str , str )
  emitItemUsed  = pyqtSignal ( QTreeWidgetItem , str             )
  emitItemFlags = pyqtSignal ( QTreeWidgetItem , str             )

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent )
    ##########################################################################
    self . StartUuid    = 1400000000000000001
    self . TablePlan    = { }
    self . Localities   = { }
    self . Listings     = { }
    self . CurrentItem  = { }
    self . isFixed      = False
    self . isActive     = False
    self . isDeletable  = False
    self . Player       = AudioPlayer ( )
    ##########################################################################
    self . insertAction = QShortcut ( QKeySequence ( Qt.Key_Insert ) , self  )
    self . deleteAction = QShortcut ( QKeySequence ( Qt.Key_Delete ) , self  )
    self . insertAction . activated . connect ( self . Insert                )
    self . deleteAction . activated . connect ( self . Delete                )
    self . emitRefresh              . connect ( self . Refresh               )
    self . emitNewItem              . connect ( self . NewItem               )
    self . emitItemUsed             . connect ( self . UpdateItemUsed        )
    self . emitItemFlags            . connect ( self . setItemFlags          )
    ##########################################################################
    self . Configure      ( )
    ##########################################################################
    return

  ############################################################################

  def Configure                           ( self                           ) :
    Labels = [ "人物名稱" , "啟用狀態" , "目前狀態" , "長編號" , "位序編號" , "" ]
    fnt    = self . font                  (                                  )
    fnt    . setPixelSize                 ( 18                               )
    self   . setFont                      ( fnt                              )
    self   . setAttribute                 ( Qt   . WA_InputMethodEnabled     )
    self   . setDragDropMode              ( self . DragDrop                  )
    self   . setRootIsDecorated           ( False                            )
    self   . setAlternatingRowColors      ( True                             )
    self   . setHorizontalScrollBarPolicy ( Qt   . ScrollBarAsNeeded         )
    self   . setVerticalScrollBarPolicy   ( Qt   . ScrollBarAsNeeded         )
    self   . setSelectionMode             ( self . ContiguousSelection       )
    self   . setColumnCount               ( 6                                )
    for      i in range                   ( 1    , 6                       ) :
      self . setColumnHidden              ( i    , True                      )
    self   . setColumnWidth               ( 5    , 5                         )
    self   . setCentralLabels             ( Labels                           )
    self   . itemDoubleClicked . connect  ( self . doubleClicked             )
    self   . itemClicked       . connect  ( self . singleClicked             )
    return

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

  def setTablePlan ( self , plan ) :
    self . TablePlan = plan
    return

  ############################################################################

  def setDeletable ( self , delx ) :
    self . isDeletable = delx
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

  def loading                 ( self                                       ) :
    ##########################################################################
    SC = SqlConnection        (                                              )
    SC . ConnectTo            ( CiosDB                                       )
    if not SC . isConnected   (                                            ) :
      return False
    ##########################################################################
    SC   . Prepare            (                                              )
    ##########################################################################
    self . LoadLocalities     ( SC                                           )
    self . LoadListings       ( SC                                           )
    ##########################################################################
    SC   . Close              (                                              )
    self . emitRefresh . emit (                                              )
    ##########################################################################
    return True

  ############################################################################

  def AddNameItem ( self , Uuid , Id , Used , Flags , Name ) :
    ##########################################################################
    it   = QTreeWidgetItem  ( [ str          ( Name  )                       ,
                                str          ( Used  )                       ,
                                self . toHex ( Flags )                       ,
                                str          ( Uuid  )                       ,
                                str          ( Id    )                       ,
                                ""                                         ] )
    ##########################################################################
    it   . setData      ( self . ColumnName  , Qt . UserRole , str ( Name  ) )
    it   . setData      ( self . ColumnUsed  , Qt . UserRole , int ( Used  ) )
    it   . setData      ( self . ColumnFlags , Qt . UserRole , int ( Flags ) )
    it   . setData      ( self . ColumnUuid  , Qt . UserRole , int ( Uuid  ) )
    it   . setData      ( self . ColumnId    , Qt . UserRole , int ( Id    ) )
    ##########################################################################
    it   . setTextAlignment ( self . ColumnUsed  , Qt . AlignRight           )
    it   . setTextAlignment ( self . ColumnFlags , Qt . AlignRight           )
    it   . setTextAlignment ( self . ColumnUuid  , Qt . AlignRight           )
    it   . setTextAlignment ( self . ColumnId    , Qt . AlignRight           )
    ##########################################################################
    self . addTopLevelItem  ( it                                             )
    ##########################################################################
    return it

  ############################################################################

  def Refresh ( self )                                                       :
    ##########################################################################
    KK  = self . Listings . keys ( )
    for u in KK                                                              :
      V = self . Listings [ u ]
      self . AddNameItem                                                     (
        str ( u             )                                                ,
        str ( V [ "Id"    ] )                                                ,
        str ( V [ "Used"  ] )                                                ,
        str ( V [ "Flags" ] )                                                ,
        str ( V [ "Name"  ] )                                                )
    ##########################################################################
    for v in range ( 0 , 5 ) :
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

  def TheName ( self , SC , Table , Uuid ) :
    LCY    = self . Locality
    NAMTAB = Table
    QQ     = f"select `name` from {NAMTAB} where ( `uuid` = {Uuid} ) and ( `locality` = {LCY} ) and ( `relevance` = 0 ) order by `priority` asc limit 0,1 ;"
    SC     . Query         ( QQ )
    NAMEX  = SC . FetchOne (    )
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

  def LoadLocalities ( self , SC ) :
    self  . Localities = { }
    Table = self . TablePlan [ "Locality" ]
    QQ    = f"select `uuid`,`code` from {Table} order by `code` asc ;"
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
    self  . Listings = {  }
    Table = self . TablePlan [ "Table" ]
    NameT = self . TablePlan [ "Name"  ]
    UUIDs = [ ]
    QQ    = f"select `uuid` from {Table} where ( `used` > 0 ) order by `uuid` asc ;"
    UUIDs = SC . ObtainUuids ( QQ )
    for u in UUIDs :
      Used  =  1
      Id    = -1
      Flags =  0
      Name  = self . TheName ( SC , NameT , u )
      QQ = f"select `id`,`used`,`state` from {Table} where ( `uuid` = {u} ) ;"
      SC       . Query         ( QQ )
      USID     = SC . FetchOne (    )
      if not ( ( not USID ) or ( USID == None  ) or ( USID is None ) ) :
        Id    = USID [ 0 ]
        Used  = USID [ 1 ]
        Flags = USID [ 2 ]
      self  . Listings [ u ] = { "Id"    : Id    ,
                                 "Used"  : Used  ,
                                 "Flags" : Flags ,
                                 "Name"  : Name  }
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
      # 項目名稱
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
      # 使用狀態
      ########################################################################
      val  = int ( item . data ( column , Qt . UserRole ) )
      sb   = QSpinBox        ( self                   )
      sb   . setMinimum      ( 0                      )
      sb   . setAlignment    ( Qt . AlignRight        )
      sb   . setValue        ( val                    )
      sb   . editingFinished . connect ( self . usedChanged )
      self . setItemWidget ( item , column , sb )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = sb
      ########################################################################
    elif ( 2 == column ) :
      ########################################################################
      # State
      ########################################################################
      le   = QLineEdit                 ( self                   )
      le   . setText                   ( item . text ( column ) )
      le   . editingFinished . connect ( self . flagsChanged    )
      self . setItemWidget             ( item , column , le     )
      self . CurrentItem [ "Item"   ] = item
      self . CurrentItem [ "Column" ] = column
      self . CurrentItem [ "Widget" ] = le
      ########################################################################
    elif ( 3 == column ) :
      ########################################################################
      # 長編號
      ########################################################################
      pass
      ########################################################################
    elif ( 4 == column ) :
      ########################################################################
      # 位序編號
      ########################################################################
      pass
      ########################################################################
    return True

  ############################################################################

  def UpdateName ( self , Item , Column , Name ) :
    ##########################################################################
    SC    = SqlConnection      (        )
    SC    . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    LCID  = self . Locality
    UID   = Item . data ( self . ColumnUuid , Qt . UserRole )
    Table = self . TablePlan [ "Name" ]
    SC    . LockWrites  ( [ Table ]                         )
    ##########################################################################
    QQ    = f"select `id` from {Table} where ( `uuid` = {UID} ) and ( `locality` = {LCID} ) and ( `relevance` = 0 ) and ( `priority` = 0 ) order by `id` asc limit 0,1 ;"
    SC    . Query ( QQ )
    RC    = SC . FetchOne (    )
    if ( ( not RC ) or ( RC == None  ) or ( RC is None ) ) :
      QQ  = f"insert into {Table} ( `uuid`,`locality`,`priority`,`relevance`,`name` ) values ( %s , %s , %s , %s , %s ) ;"
      SC  . QueryValues     ( QQ , ( UID , LCID , 0 , 0 , Name , ) )
      QQ  = f"update {Table} set `length` = length(`name`) where ( `uuid` = {UID} ) and ( `locality` = {LCID} ) and ( `relevance` = 0 ) and ( `priority` = 0 ) ;"
      SC  . Query ( QQ )
    else :
      Id  = RC [ 0 ]
      QQ  = f"update {Table} set `name` = %s where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
      SC  . QueryValues     ( QQ , ( Name , ) )
      QQ  = f"update {Table} set `length` = length(`name`) where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
      SC  . Query ( QQ )
    ##########################################################################
    SC    . UnlockTables    (                 )
    ##########################################################################
    SC    . Close           (           )
    ##########################################################################
    self  . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
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
    item   . setText              ( column , Name )
    threading . Thread ( target = self . UpdateName , args = ( item , column , Name , ) ) . start ( )
    return True

  ############################################################################

  def UpdateItemUsed ( self , Item , Used ) :
    Item . setText ( self . ColumnUsed ,                 str ( Used ) )
    Item . setData ( self . ColumnUsed , Qt . UserRole , int ( Used ) )
    return

  def UpdateUsed ( self , Item , Used ) :
    ##########################################################################
    SC = SqlConnection      (        )
    SC . ConnectTo          ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (        )
    ##########################################################################
    UID   = Item . data ( self . ColumnUuid , Qt . UserRole )
    Table = self . TablePlan [ "Table" ]
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    QQ    = f"update {Table} set `used` = {Used} where ( `uuid` = {UID} ) ;"
    SC    . Query         ( QQ )
    ##########################################################################
    SC    . UnlockTables  (    )
    ##########################################################################
    SC    . Close         (    )
    ##########################################################################
    self  . emitItemUsed . emit ( Item , str ( Used ) )
    ##########################################################################
    self  . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  def usedChanged ( self ) :
    if ( "Item"   not in self . CurrentItem ) :
      return False
    if ( "Column" not in self . CurrentItem ) :
      return False
    if ( "Widget" not in self . CurrentItem ) :
      return False
    item   = self   . CurrentItem [ "Item"   ]
    column = self   . CurrentItem [ "Column" ]
    widget = self   . CurrentItem [ "Widget" ]
    Used   = widget . value       (          )
    self   . removeParked         (          )
    oldUsed = item . data  ( column , Qt . UserRole )
    oldUsed = int          ( oldUsed                )
    if ( Used == oldUsed ) :
      return False
    threading . Thread ( target = self . UpdateUsed , args = ( item , Used , ) ) . start ( )
    return True

  ############################################################################

  def UpdateFlags ( self , Item , Column , Uuid , Flags ) :
    ##########################################################################
    SC    = SqlConnection   (        )
    SC    . ConnectTo       ( CiosDB )
    if not SC . isConnected (        ) :
      return False
    ##########################################################################
    SC    . Prepare         (           )
    ##########################################################################
    Table = self . TablePlan [ "Table" ]
    QQ    = f"update {Table} set `state` = {Flags} where ( `uuid` = {Uuid} ) ;"
    SC    . LockWrites      ( [ Table ] )
    SC    . Query           ( QQ        )
    SC    . UnlockTables    (           )
    ##########################################################################
    SC    . Close           (           )
    ##########################################################################
    HEX   = self . toHex    ( Flags                 )
    self  . emitItemFlags . emit ( Item , HEX )
    ##########################################################################
    self  . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
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
    UID = item . data ( self . ColumnUuid , Qt . UserRole )
    threading . Thread ( target = self . UpdateFlags , args = ( item , column , UID , V , ) ) . start ( )
    return True

  ############################################################################

  def NewItem ( self , Uuid , Id , Used , Flags , Name )                     :
    ##########################################################################
    it = self . AddNameItem                                                  (
           str ( Uuid  )                                                     ,
           str ( Id    )                                                     ,
           str ( Used  )                                                     ,
           str ( Flags )                                                     ,
           str ( Name  )                                                     )
    self . setCurrentItem ( it )
    ##########################################################################
    self . Player . Play  ( "D:/CIOS/Sounds/CIOS/append.mp3" )
    ##########################################################################
    return True

  ############################################################################

  def AppendItem ( self ) :
    if ( self . isFixed ) :
      return False
    ##########################################################################
    SC = SqlConnection       (        )
    SC . ConnectTo           ( CiosDB )
    if not SC . isConnected  (        ) :
      return False
    ##########################################################################
    SC    . Prepare          (        )
    ##########################################################################
    UID      = self . StartUuid
    TID      = 7
    LCID     = self . Locality
    Table    = self . TablePlan [ "Table" ]
    Primary  = self . TablePlan [ "Major" ]
    NameT    = self . TablePlan [ "Name"  ]
    ##########################################################################
    SC       . LockWrites    ( [ Table , Primary , NameT ] )
    ##########################################################################
    QQ      = f"select `uuid` from {Table} order by `uuid` desc limit 0,1 ;"
    SC      . Query         ( QQ )
    XC      = SC . FetchOne (    )
    if not ( ( not XC ) or ( XC == None  ) or ( XC is None ) ) :
      UID   = XC [ 0 ]
    UID     = UID + 1
    QQ      = f"insert into {Primary} ( `uuid`,`type`,`used` ) values ( {UID},{TID},1 ) ;" ;
    SC      . Query         ( QQ )
    QQ      = f"insert into {Table} ( `uuid`,`used` ) values ( {UID} , 1 ) ;" ;
    SC      . Query         ( QQ )
    ##########################################################################
    QQ       = f"select `id`,`used`,`state` from {Table} where ( `uuid` = {UID} ) ;"
    SC       . Query         ( QQ )
    RC       = SC . FetchOne (    )
    ##########################################################################
    Name     = self . TheName ( SC , NameT , UID )
    ##########################################################################
    SC       . UnlockTables  (           )
    SC       . Close         (           )
    ##########################################################################
    if not ( ( not RC ) or ( RC == None  ) or ( RC is None ) ) :
      Id    = RC [ 0 ]
      Used  = RC [ 1 ]
      Flags = RC [ 2 ]
      self . emitNewItem . emit                                              (
        str ( UID   )                                                        ,
        str ( Id    )                                                        ,
        str ( Used  )                                                        ,
        str ( Flags )                                                        ,
        str ( Name  )                                                        )
    ##########################################################################
    return True

  ############################################################################

  def Insert ( self ) :
    threading . Thread ( target = self . AppendItem ) . start ( )
    return True

  ############################################################################

  def RemoveItem ( self , UID ) :
    ##########################################################################
    SC       = SqlConnection   (        )
    SC       . ConnectTo       ( CiosDB )
    if not SC . isConnected    (        ) :
      return False
    ##########################################################################
    SC       . Prepare         (        )
    ##########################################################################
    Table    = self . TablePlan [ "Table" ]
    Primary  = self . TablePlan [ "Major" ]
    ##########################################################################
    SC       . LockWrites      ( [ Table , Primary ] )
    ##########################################################################
    QQ       = f"delete from {Primary} where ( `uuid` = {UID} ) ;"
    SC       . Query           ( QQ        )
    ##########################################################################
    QQ       = f"delete from {Table} where ( `uuid` = {UID} ) ;"
    SC       . Query           ( QQ        )
    ##########################################################################
    SC       . UnlockTables    (           )
    SC       . Close           (           )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/delete.mp3" )
    ##########################################################################
    return True

  ############################################################################

  def DeleteItem ( self , item ) :
    if ( not self . isDeletable ) :
      return False
    UID = item . data ( self . ColumnUuid , Qt . UserRole )
    idx = self . indexOfTopLevelItem ( item )
    if ( idx >= 0 ) :
      self . takeTopLevelItem ( idx )
      threading . Thread ( target = self . RemoveItem , args = ( UID , ) ) . start ( )
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
    ##########################################################################
    MM           = MenuManager ( self )
    ##########################################################################
    id           = 0
    hit          = self . headerItem ( )
    MenuMap      = { }
    item         = self    . itemAt  ( pos )
    atPos        = QCursor . pos     (     )
    ##########################################################################
    reloadAction = MM . addAction    ( 1000 , "重新載入" )
    MM                . addSeparator ( )
    CNT          = 0
    if not ( self . isFixed ) :
      appendAction = MM . addAction    ( 1001 , "新增" )
      CNT        = CNT + 1
    ##########################################################################
    if ( self . isDeletable ) :
      if ( None == item ) :
        pass
      else :
        deleteAction = MM  . addAction ( 1002 , "刪除" )
        id = item . data ( 5 , Qt . UserRole )
        CNT        = CNT + 1
    ##########################################################################
    if ( CNT > 0 ) :
      MM . addSeparator ( )
    ##########################################################################
    idAction = MM . addAction ( 1003 , "排序" , True , self . isSortingEnabled ( ) )
    MM . addSeparator ( )
    ##########################################################################
    columnMenu = MM . addMenu ( "顯示欄位" )
    for x in range ( 1 , 6 ) :
      idShown  = not self . isColumnHidden ( x )
      idName   = hit  . text ( x )
      if ( len ( idName ) <= 0 ) :
        idName = "結尾填白"
      idAction = MM . addActionFromMenu ( columnMenu , 2000000 + x , idName , True , idShown )
    ##########################################################################
    languageMenu = MM . addMenu ( "內定語言" )
    KK  = self . Localities . keys ( )
    for x in KK :
      idName    = self . Localities [ x ]
      idShown   = False
      if ( self . Locality == x ) :
        idShown = True
      act = MM . addActionFromMenu ( languageMenu , 1000000 + x , idName , True , idShown )
    ##########################################################################
    self   . Player . Play ( "D:/CIOS/Sounds/CIOS/open.mp3" )
    MM     . setFont    ( self . font ( ) )
    action = MM . exec_ ( atPos           )
    ##########################################################################
    if ( None == action ) :
      return False
    ##########################################################################
    MenuId = MM [ action ]
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
    elif ( MenuId > 1000000 ) and ( MenuId < 2000000 ) :
      self . Locality    = MenuId - 1000000
      self . startup ( )
    elif ( MenuId > 2000000 ) and ( MenuId < 3000000 ) :
      idShown = action . isChecked ( )
      idx     = MenuId - 2000000
      if ( idShown ) :
        self . setColumnHidden        ( idx , False )
        self . resizeColumnToContents ( idx         )
      else :
        self . setColumnHidden        ( idx , True  )
    ##########################################################################
    return True

  ############################################################################

##############################################################################
