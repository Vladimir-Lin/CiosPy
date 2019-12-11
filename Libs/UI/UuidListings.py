import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
##############################################################################
import pyttsx3
from   playsound                      import playsound
import urllib
import urllib . parse
from   pathlib                        import Path
import win32com . client
##############################################################################
import mysql    . connector
from   mysql    . connector           import Error
##############################################################################
import Actions
from   Actions                        import *
##############################################################################
import CIOS
from   CIOS  . SQL                    import SqlQuery
from   CIOS  . SQL                    import SqlConnection
from   CIOS  . Database               import Tables
from   CIOS  . Voice     . Recognizer import Recognizer
from   CIOS  . Voice     . Audio      import AudioPlayer
from   CIOS  . Documents . JSON       import Load  as LoadJSON
from   CIOS  . Documents . JSON       import Merge as MergeJSON
from   CIOS  . Documents . Commands   import CommandsMapper
##############################################################################
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
from   CIOS  . Qt . VirtualGui        import VirtualGui
from   CIOS  . Qt . MenuManager       import MenuManager
from   CIOS  . Qt . TreeWidget        import TreeWidget
##############################################################################

class UuidListings ( TreeWidget ) :

  ############################################################################

  ColumnName        = 0
  ColumnUsed        = 1
  ColumnUuid        = 2
  ColumnId          = 3
  ColumnEmpty       = 4

  ############################################################################

  emitRefresh   = pyqtSignal (                       )
  emitItemFlags = pyqtSignal ( QTreeWidgetItem , str )
  emitNewItem   = pyqtSignal ( str , str , str , str )
  emitItemUsed  = pyqtSignal ( QTreeWidgetItem , str )

  ############################################################################

  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent )
    ##########################################################################
    self . insertAction = QShortcut ( QKeySequence ( Qt.Key_Insert ) , self  )
    self . deleteAction = QShortcut ( QKeySequence ( Qt.Key_Delete ) , self  )
    self . insertAction . activated . connect ( self . Insert                )
    self . deleteAction . activated . connect ( self . Delete                )
    self . emitRefresh              . connect ( self . Refresh               )
    self . emitItemFlags            . connect ( self . setItemFlags          )
    self . emitNewItem              . connect ( self . NewItem               )
    self . emitItemUsed             . connect ( self . UpdateItemUsed        )
    ##########################################################################
    self . Database     = ""
    self . Table        = ""
    self . Primary      = ""
    self . Names        = ""
    self . StartUuid    = 0
    self . TypeId       = 0
    self . StartId      = 0
    self . PageSize     = 25
    self . Items        = 0
    self . isUsed       = False
    self . isFixed      = False
    self . isActive     = False
    self . isDeletable  = False
    self . Player       = AudioPlayer ( )
    self . Localities   = { }
    self . Listings     = { }
    self . CurrentItem  = { }
    self . Configure      ( )
    ##########################################################################

  ############################################################################

  def Configure ( self ) :
    Labels = [ "項目名稱" , "使用狀態" , "長編號" , "位序編號" , "" ]
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
    self   . setColumnCount               ( 5                            )
    for i in range ( 1 , 4 ) :
      self . setColumnHidden              ( i    , True                  )
    self   . setColumnWidth               ( 4    , 5                     )
    self   . setHeaderLabels              ( Labels                       )
    self   . itemDoubleClicked . connect  ( self . doubleClicked         )
    self   . itemClicked       . connect  ( self . singleClicked         )

  ############################################################################

  def setStartUuid ( self , startUuid ) :
    self . StartUuid = startUuid
    return True

  ############################################################################

  def setTypeId ( self , typeId ) :
    self . TypeId = typeId
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

  def setPrimary ( self , primary ) :
    self . Primary = primary
    return True

  ############################################################################

  def setNames ( self , names ) :
    self . Names = names
    return True

  ############################################################################

  def setUsed ( self , used ) :
    self . isUsed = used
    return True

  ############################################################################

  def setFixed ( self , fixed ) :
    self . isFixed = fixed
    return True

  ############################################################################

  def setActive ( self , active ) :
    self . isActive = active
    return True

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

  def TheName ( self , SC , Table , Uuid ) :
    LCY    = self . Locality
    DBS    = self . Database
    NAMTAB = f"`{DBS}`.`{Table}`"
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
    self  . Listings = {  }
    DBS   = self . Database
    TBS   = self . Table
    Table = f"`{DBS}`.`{TBS}`"
    UUIDs = [ ]
    if ( self . isUsed ) :
      if ( self . isActive ) :
        QQ    = f"select `uuid` from {Table} where ( `used` > 0 ) order by `id` asc ;"
        UUIDs = SC . ObtainUuids ( QQ )
      else :
        QQ    = f"select `uuid` from {Table} order by `id` asc ;"
        UUIDs = SC . ObtainUuids ( QQ )
    else :
      QQ    = f"select `uuid` from {Table} order by `id` asc ;"
      UUIDs = SC . ObtainUuids ( QQ )
    for u in UUIDs :
      Used = 1
      Id   = -1
      Name = self . TheName ( SC , self . Names , u )
      if ( self . isUsed ) :
        QQ = f"select `id`,`used` from {Table} where ( `uuid` = {u} ) ;"
        SC       . Query         ( QQ )
        USID     = SC . FetchOne (    )
        if not ( ( not USID ) or ( USID == None  ) or ( USID is None ) ) :
          Id   = USID [ 0 ]
          Used = USID [ 1 ]
      else :
        QQ = f"select `id` from {Table} where ( `uuid` = {u} ) ;"
        SC       . Query         ( QQ )
        USID     = SC . FetchOne (    )
        if not ( ( not USID ) or ( USID == None  ) or ( USID is None ) ) :
          Id   = USID [ 0 ]
      self  . Listings [ u ] = { "Id" : Id , "Used" : Used , "Name" : Name }
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
    self . LoadLocalities     ( SC     )
    self . LoadListings       ( SC     )
    ##########################################################################
    SC   . Close              (        )
    self . emitRefresh . emit (        )
    ##########################################################################
    return True

  ############################################################################

  def AddNameItem ( self , Uuid , Id , Used , Name ) :
    ##########################################################################
    it   = QTreeWidgetItem  ( [ str ( Name )                                 ,
                                str ( Used )                                 ,
                                str ( Uuid )                                 ,
                                str ( Id   )                                 ,
                                ""                                         ] )
    ##########################################################################
    it   . setData        ( self . ColumnName , Qt . UserRole , str ( Name ) )
    it   . setData        ( self . ColumnUsed , Qt . UserRole , int ( Used ) )
    it   . setData        ( self . ColumnUuid , Qt . UserRole , int ( Uuid ) )
    it   . setData        ( self . ColumnId   , Qt . UserRole , int ( Id   ) )
    ##########################################################################
    it   . setTextAlignment ( self . ColumnUsed , Qt . AlignRight            )
    it   . setTextAlignment ( self . ColumnUuid , Qt . AlignRight            )
    it   . setTextAlignment ( self . ColumnId   , Qt . AlignRight            )
    ##########################################################################
    self . addTopLevelItem  ( it                                             )
    ##########################################################################
    return it

  ############################################################################

  def Refresh ( self )                                                       :
    ##########################################################################
    KK = self . Listings . keys ( )
    for u in KK                                                              :
      V = self . Listings [ u ]
      self . AddNameItem                                                     (
        str ( u            )                                                 ,
        str ( V [ "Id"   ] )                                                 ,
        str ( V [ "Used" ] )                                                 ,
        str ( V [ "Name" ] )                                                 )
    ##########################################################################
    for v in range ( 0 , 4 ) :
      self . resizeColumnToContents ( v )
    ##########################################################################
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
      # 長編號
      ########################################################################
      pass
      ########################################################################
    elif ( 3 == column ) :
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
    DBS   = self . Database
    TBS   = self . Names
    LCID  = self . Locality
    UID   = Item . data ( self . ColumnUuid , Qt . UserRole )
    Table = f"`{DBS}`.`{TBS}`"
    SC    . LockWrites      ( [ Table ]       )
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
    DBS   = self . Database
    TBS   = self . Table
    UID   = Item . data ( self . ColumnUuid , Qt . UserRole )
    Table = f"`{DBS}`.`{TBS}`"
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

  def NewItem ( self , Uuid , Id , Used , Name )                             :
    ##########################################################################
    it = self . AddNameItem                                                  (
           str ( Uuid )                                                      ,
           str ( Id   )                                                      ,
           str ( Used )                                                      ,
           str ( Name )                                                      )
    self . setCurrentItem ( it )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/append.mp3" )
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
    DBS      = self . Database
    TBS      = self . Table
    PBS      = self . Primary
    UID      = self . StartUuid
    TID      = self . TypeId
    LCID     = self . Locality
    Table    = f"`{DBS}`.`{TBS}`"
    Primary  = f"`{DBS}`.`{PBS}`"
    ##########################################################################
    SC       . LockWrites    ( [ Table ] )
    ##########################################################################
    QQ      = f"select `uuid` from {Table} order by `uuid` desc limit 0,1 ;"
    XC      = SC . FetchOne (    )
    if not ( ( not XC ) or ( XC == None  ) or ( XC is None ) ) :
      UID   = XC [ 0 ]
    UID     = UID + 1
    QQ      = f"insert into {Primary} ( `uuid`,`type`,`used` ) values ( {UID},{TID},1 ) ;" ;
    SC      . Query         ( QQ )
    QQ      = f"insert into {Table} ( `uuid` ) values ( {UID} ) ;" ;
    SC      . Query         ( QQ )
    ##########################################################################
    QQ       = f"select `id`,`used` from {Table} where ( `uuid` = {UID} ) ;"
    SC       . Query         ( QQ )
    RC       = SC . FetchOne (    )
    ##########################################################################
    Name     = self . TheName ( SC , self . Names , UID )
    ##########################################################################
    SC       . UnlockTables  (           )
    SC       . Close         (           )
    ##########################################################################
    if not ( ( not RC ) or ( RC == None  ) or ( RC is None ) ) :
      Id    = RC [ 0 ]
      Used  = RC [ 1 ]
      self . emitNewItem . emit                                              (
        str ( UID  )                                                         ,
        str ( Id   )                                                         ,
        str ( Used )                                                         ,
        str ( Name )                                                         )
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
    # TBS   = self . Table
    # UID   = self . Uuid
    # Table = f"`{DBS}`.`{TBS}`"
    ##########################################################################
    SC    . LockWrites      ( [ Table ] )
    ##########################################################################
    # QQ    = f"delete from {Table} where ( `id` = {Id} ) and ( `uuid` = {UID} ) ;"
    # SC    . Query           ( QQ        )
    ##########################################################################
    SC    . UnlockTables    (           )
    SC    . Close           (           )
    ##########################################################################
    self . Player . Play ( "D:/CIOS/Sounds/CIOS/delete.mp3" )
    ##########################################################################
    return True

  ############################################################################

  def DeleteItem ( self , item ) :
    if ( not self . isDeletable ) :
      return False
    # Id = item . data ( 5 , Qt . UserRole )
    # idx = self . indexOfTopLevelItem ( item )
    # if ( idx >= 0 ) :
    #   self . takeTopLevelItem ( idx )
    #   threading . Thread ( target = self . RemoveItem , args = ( Id , ) ) . start ( )
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
    for x in range ( 1 , 5 ) :
      if ( x == 1 ) :
        if ( not self . isUsed ) :
          continue
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

if __name__ == '__main__':
  ############################################################################
  Width     = 480
  Height    = 960
  Locality  = 1002
  StartUuid = 0
  typeId    = 0
  Title     = ""
  Table     = ""
  Primary   = ""
  NameTable = ""
  Database  = "cios"
  Used      = False
  Fixed     = False
  Active    = False
  Deletable = False
  ############################################################################
  argv = sys . argv [ 1: ]
  ############################################################################
  try                                                                        :
    opts, args = getopt . getopt                                             (
                   argv                                                      ,
                   "afurw:h:s:i:l:d:c:p:n:t:"                                ,
                   [ "width="                                                ,
                     "height="                                               ,
                     "start="                                                ,
                     "typeid="                                               ,
                     "locality="                                             ,
                     "active"                                                ,
                     "fixed"                                                 ,
                     "used"                                                  ,
                     "remove"                                                ,
                     "database="                                             ,
                     "caption="                                              ,
                     "primary="                                              ,
                     "name="                                                 ,
                     "table="                                              ] )
  except getopt . GetoptError                                                :
    sys . exit ( 1 )
  ############################################################################
  for opt, arg in opts                                                       :
    if   opt in ( "-w" , "--width"    )                                      :
      Width     = int ( arg )
    elif opt in ( "-h" , "--height"   )                                      :
      Height    = int ( arg )
    elif opt in ( "-l" , "--locality" )                                      :
      Locality  = arg
    elif opt in ( "-s" , "--start"    )                                      :
      StartUuid = arg
    elif opt in ( "-s" , "--typeid"   )                                      :
      typeId    = int ( arg )
    elif opt in ( "-d" , "--database" )                                      :
      Database  = arg
    elif opt in ( "-c" , "--caption"  )                                      :
      Title     = arg
    elif opt in ( "-a" , "--active"   )                                      :
      Active    = True
    elif opt in ( "-r" , "--remove"   )                                      :
      Deletable = True
    elif opt in ( "-u" , "--used"     )                                      :
      Used      = True
    elif opt in ( "-f" , "--fixed"    )                                      :
      Fixed     = True
    elif opt in ( "-t" , "--table"    )                                      :
      Table     = arg
    elif opt in ( "-p" , "--primary"  )                                      :
      Primary   = arg
    elif opt in ( "-n" , "--name"     )                                      :
      NameTable = arg
  ############################################################################
  if                      ( len ( Table     ) <=  0                        ) :
    sys  . exit           ( 0                                                )
  if                      ( len ( Primary   ) <=  0                        ) :
    sys  . exit           ( 0                                                )
  if                      ( len ( NameTable ) <=  0                        ) :
    sys  . exit           ( 0                                                )
  if                      ( typeId            <=  0                        ) :
    sys  . exit           ( 0                                                )
  ############################################################################
  app    = QApplication   ( sys . argv                                       )
  w      = UuidListings   (                                                  )
  w      . setWindowTitle ( Title                                            )
  w      . resize         ( Width , Height                                   )
  w      . show           (                                                  )
  w      . setStartUuid   ( StartUuid                                        )
  w      . setTypeId      ( typeId                                           )
  w      . setDatabase    ( Database                                         )
  w      . setTable       ( Table                                            )
  w      . setPrimary     ( Primary                                          )
  w      . setNames       ( NameTable                                        )
  w      . setActive      ( Active                                           )
  w      . setUsed        ( Used                                             )
  w      . setFixed       ( Fixed                                            )
  w      . setDeletable   ( Deletable                                        )
  w      . setLocality    ( Locality                                         )
  w      . startup        (                                                  )
  sys    . exit           ( app . exec_ ( )                                  )
  ############################################################################
