import os
import sys
import getopt
import time
import requests
import threading
import gettext
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
from PyQt5.QtGui import QCursor
from PyQt5 import QtGui, QtCore

def ActualFile ( filename ) :
  return os . path . dirname ( os . path . abspath (__file__) ) + "/" + filename

def RunSystem ( Program ) :
  os   . system ( "start " + Program )

class SystemTrayIcon ( QSystemTrayIcon ) :

  def __init__(self, icon, parent=None):
    QSystemTrayIcon . __init__ ( self , icon , parent )
    self . setToolTip ( "CIOS系統選單" )
    self . activated . connect ( self . onTrayActivated )
    # Configure Menu
    menu          = QMenu ( parent )
    # CIOS Packages
    qtMenu        = menu      . addMenu ( "Qt" )
    taskMenu      = menu      . addMenu ( "任務管理系統" )
    peopleMenu    = menu      . addMenu ( "人物管理系統" )
    galleryMenu   = menu      . addMenu ( "圖庫管理系統" )
    videoMenu     = menu      . addMenu ( "視訊管理系統" )
    audioMenu     = menu      . addMenu ( "音訊管理系統" )
    modelMenu     = menu      . addMenu ( "物體模型系統" )
    scienceMenu   = menu      . addMenu ( "科學試算系統" )
    databaseMenu  = menu      . addMenu ( "資料庫系統" )
    depotMenu     = menu      . addMenu ( "軟體倉庫" )
    menu          . addSeparator ( )
    # Development System
    devMenu       = menu      . addMenu ( "開發環境" )
    eclipseMenu   = devMenu   . addMenu ( "Eclipse" )
    mingwMenu     = devMenu   . addMenu ( "MinGW" )
    # SQL System
    sqlMenu       = menu      . addMenu ( "資料庫系統" )
    # External Packages
    pkgMenu        = menu     . addMenu ( "外部套件" )
    mathExtraMenu  = pkgMenu  . addMenu ( "數學處理套件" )
    imageExtraMenu = pkgMenu  . addMenu ( "影像處理套件" )
    avExtraMenu    = pkgMenu  . addMenu ( "影音處理套件" )
    m3dAction      = pkgMenu  . addMenu ( "物體模型系統" )
    edaAction      = pkgMenu  . addMenu ( "電子電路設計" )
    # Qt
    creatorAction  = qtMenu . addAction ( "Qt Creator" )
    creatorAction  . triggered . connect ( self . qtCreator )
    # Eclipse
    # Java
    eclipseJavaAction = eclipseMenu . addAction ( "Java" )
    eclipseJavaAction . triggered . connect ( self . eclipseJava )
    # Jee
    eclipseJeeAction = eclipseMenu . addAction ( "Jee" )
    eclipseJeeAction . triggered . connect ( self . eclipseJee )
    # Cpp
    eclipseCppAction = eclipseMenu . addAction ( "C++" )
    eclipseCppAction . triggered . connect ( self . eclipseCpp )
    # Javascript
    eclipseJsAction = eclipseMenu . addAction ( "Javascript" )
    eclipseJsAction . triggered . connect ( self . eclipseJs )
    # PHP
    eclipsePhpAction = eclipseMenu . addAction ( "PHP" )
    eclipsePhpAction . triggered . connect ( self . eclipsePhp )
    # Scout
    eclipseScoutAction = eclipseMenu . addAction ( "Scout" )
    eclipseScoutAction . triggered . connect ( self . eclipseScout )
    # Rust
    eclipseRustAction = eclipseMenu . addAction ( "Rust" )
    eclipseRustAction . triggered . connect ( self . eclipseRust )
    # Parallel
    eclipseParallelAction = eclipseMenu . addAction ( "Parallel" )
    eclipseParallelAction . triggered . connect ( self . eclipseParallel )
    # Modeling
    eclipseModelingAction = eclipseMenu . addAction ( "Modeling" )
    eclipseModelingAction . triggered . connect ( self . eclipseModeling )
    # RCP
    eclipseRcpAction = eclipseMenu . addAction ( "RCP" )
    eclipseRcpAction . triggered . connect ( self . eclipseRcp )
    # MSYS
    msysAction = mingwMenu . addAction ( "MSYS" )
    msysAction . triggered . connect ( self . MSYS )
    # MinGW
    mingwAction = mingwMenu . addAction ( "MinGW" )
    mingwAction . triggered . connect ( self . MinGW )
    # CMake
    cMakeAction = devMenu . addAction ( "CMake" )
    cMakeAction . triggered . connect ( self . devCMake )
    # NSIS
    nsisAction = devMenu . addAction ( "NSIS" )
    nsisAction . triggered . connect ( self . devNSIS )
    # Venis
    venisAction = devMenu . addAction ( "Venis IX" )
    venisAction . triggered . connect ( self . devVenis )
    # HeidiSQL
    heidiAction = sqlMenu . addAction ( "Heidi SQL" )
    heidiAction . triggered . connect ( self . Heidi )
    # AWS
    awsAction = sqlMenu . addAction ( "AWS" )
    awsAction . triggered . connect ( self . AWS )
    # local
    localAction = sqlMenu . addAction ( "192.168.0.98" )
    localAction . triggered . connect ( self . Local )
    # backup
    backupAction = sqlMenu . addAction ( "192.168.0.97" )
    backupAction . triggered . connect ( self . BackupSQL )
    # 數學處理套件
    # Scilab
    scilabAction = mathExtraMenu . addAction ( "Scilab" )
    scilabAction . triggered . connect ( self . Scilab )
    # R
    rlangAction = mathExtraMenu . addAction ( "R" )
    rlangAction . triggered . connect ( self . RLang )
    # 影像處理套件
    # GIMP
    gimpAction = imageExtraMenu . addAction ( "GIMP" )
    gimpAction . triggered . connect ( self . GIMP )
    # Inkscape
    inkscapeAction = imageExtraMenu . addAction ( "SVG向量圖編輯 Inkscape" )
    inkscapeAction . triggered . connect ( self . Inkscape )
    # ImageGlass
    imageGlassAction = imageExtraMenu . addAction ( "圖片瀏覽 Image Glass" )
    imageGlassAction . triggered . connect ( self . ImageGlass )
    # XnConvert
    xnConvertAction = imageExtraMenu . addAction ( "圖片轉檔 XnConvert" )
    xnConvertAction . triggered . connect ( self . XnConvert )
    # 影音處理套件
    # GOM System
    gomMenu       = avExtraMenu . addMenu ( "GOM" )
    # GOM Remote
    gomRemoteAction = gomMenu . addAction ( "GOM Remote" )
    gomRemoteAction . triggered . connect ( self . gomRemote )
    # GOM Player
    gomPlayerAction = gomMenu . addAction ( "GOM Player" )
    gomPlayerAction . triggered . connect ( self . gomPlayer )
    # GOM Audio
    gomAudioAction = gomMenu . addAction ( "GOM Audio" )
    gomAudioAction . triggered . connect ( self . gomAudio )
    # GOM Cam
    gomCamAction = gomMenu . addAction ( "GOM Cam" )
    gomCamAction . triggered . connect ( self . gomCam )
    # GOM Encoder
    gomEncoderAction = gomMenu . addAction ( "GOM Encoder" )
    gomEncoderAction . triggered . connect ( self . gomEncoder )
    # GOM Mix
    gomMixAction = gomMenu . addAction ( "GOM Mix" )
    gomMixAction . triggered . connect ( self . gomMix )
    # SMPlayer
    mplayerAction = avExtraMenu . addAction("SMPlayer")
    mplayerAction . setIcon ( QIcon ( ActualFile ( "images/64x64/play.png" ) ) )
    mplayerAction . triggered . connect ( self . SMPlayer )
    # Drax
    draxAction    = avExtraMenu . addAction ( "Drax" )
    draxAction    . triggered . connect ( self . Drax )
    # Aegisub
    aegisubAction = avExtraMenu . addAction ( "Aegisub" )
    aegisubAction . triggered . connect ( self . Aegisub )
    # AV IDE Mux
    draxAction    = avExtraMenu . addAction ( "AV IDE Mux" )
    draxAction    . triggered . connect ( self . AvIDEmux )
    # Audacity
    audacityAction = avExtraMenu . addAction ( "Audacity" )
    audacityAction . triggered . connect ( self . Audacity )
    # CamStudio
    camStudioAction = avExtraMenu . addAction ( "CamStudio" )
    camStudioAction . triggered . connect ( self . CamStudio )
    # Blender
    blenderAction = m3dAction . addAction ( "Blender" )
    blenderAction . triggered . connect ( self . Blender )
    # KiCad
    KiCadAction = edaAction . addAction ( "KiCad" )
    KiCadAction . triggered . connect ( self . KiCad )
    # Packages Menu
    menu          . addSeparator ( )
    # Restart
    restartAction = menu      . addAction("重新啟動")
    restartAction . triggered . connect ( self . Restart )
    # Exit
    exitAction    = menu      . addAction ( "離開" )
    exitAction    . setIcon ( QIcon ( ActualFile ( "images/24x24/delete.png" ) ) )
    exitAction    . triggered . connect ( self . Quit )
    self . setContextMenu ( menu )
    self . Menu = menu

  def onTrayActivated ( self , reason ) :
    if ( reason == 3 ) :
      self . Menu . exec_ ( QCursor . pos ( ) )

  def Restart ( self ) :
    rstv = ActualFile ( "Restart.py" )
    os   . system ( "start python " + rstv )
    self . hide ( )
    qApp . quit ( )

  def Quit ( self ) :
    self . hide ( )
    qApp . quit ( )

  def SMPlayer ( self ) :
    RunSystem ( "D:/Programs/SMPlayer/smplayer.exe" )

  def Drax ( self ) :
    RunSystem ( "D:/Programs/Drax/Drax/start.bat" )

  def Aegisub ( self ) :
    RunSystem ( "D:/Programs/Aegisub/aegisub32.exe" )

  def AvIDEmux ( self ) :
    RunSystem ( "D:/Programs/Avidemux/2.7/avidemux.exe" )

  def Audacity ( self ) :
    RunSystem ( "D:/Programs/Audacity/audacity.exe" )

  def CamStudio ( self ) :
    RunSystem ( "D:/Programs/CamStudio/2.7/Recorder.exe" )

  def gomRemote ( self ) :
    RunSystem ( "D:/Programs/GRETECH/GOMRemote/GomRemote2.exe" )

  def gomPlayer ( self ) :
    RunSystem ( "D:/Programs/GRETECH/GOMPlayer/GOM.exe" )

  def gomAudio ( self ) :
    RunSystem ( "D:/Programs/GRETECH/GOMAudio/Goma.exe" )

  def gomCam ( self ) :
    RunSystem ( "D:/Programs/GOM/GOMCam/GOMCam.exe" )

  def gomEncoder ( self ) :
    RunSystem ( "D:/Programs/GRETECH/GOMEncoder/GomEnc.exe" )

  def gomMix ( self ) :
    RunSystem ( "D:/Programs/GOM/GOMMixPro/GomMixProMain.exe" )

  def eclipseJava ( self ) :
    RunSystem ( "D:/Programs/Eclipse/java-2019-03/eclipse/eclipse.exe" )

  def eclipseJee ( self ) :
    RunSystem ( "D:/Programs/Eclipse/jee-2019-03/eclipse/eclipse.exe" )

  def eclipseCpp ( self ) :
    RunSystem ( "D:/Programs/Eclipse/cpp-2019-03/eclipse/eclipse.exe" )

  def eclipseJs ( self ) :
    RunSystem ( "D:/Programs/Eclipse/javascript-2019-03/eclipse/eclipse.exe" )

  def eclipsePhp ( self ) :
    RunSystem ( "D:/Programs/Eclipse/php-2019-03/eclipse/eclipse.exe" )

  def eclipseModeling ( self ) :
    RunSystem ( "D:/Programs/Eclipse/modeling-2019-03/eclipse/eclipse.exe" )

  def eclipseRcp ( self ) :
    RunSystem ( "D:/Programs/Eclipse/rcp-2019-03/eclipse/eclipse.exe" )

  def eclipseParallel ( self ) :
    RunSystem ( "D:/Programs/Eclipse/parallel-2019-03/eclipse/eclipse.exe" )

  def eclipseScout ( self ) :
    RunSystem ( "D:/Programs/Eclipse/scout-2019-03/eclipse/eclipse.exe" )

  def eclipseRust ( self ) :
    RunSystem ( "D:/Programs/Eclipse/rust-2019-03/eclipse/eclipse.exe" )

  def devCMake ( self ) :
    RunSystem ( "D:/Programs/CMake/bin/cmake-gui.exe" )

  def devNSIS ( self ) :
    RunSystem ( "D:/Programs/NSIS/NSIS.exe" )

  def devVenis ( self ) :
    RunSystem ( "D:/Programs/Venis/Venis.exe" )

  def GIMP ( self ) :
    RunSystem ( "D:/Programs/GIMP/2/bin/gimp-2.10.exe" )

  def Inkscape ( self ) :
    RunSystem ( "D:/Programs/Inkscape/inkscape.exe" )

  def ImageGlass ( self ) :
    RunSystem ( "D:/Programs/ImageGlass/ImageGlass.exe" )

  def XnConvert ( self ) :
    RunSystem ( "D:/Programs/XnConvert/xnconvert.exe" )

  def Blender ( self ) :
    RunSystem ( "D:/Programs/Blender/blender.exe" )

  def RLang ( self ) :
    RunSystem ( "D:/Programs/R/bin/x64/Rgui.exe" )

  def Scilab ( self ) :
    RunSystem ( "D:/Programs/SciLab/bin/WScilex.exe" )

  def KiCad ( self ) :
    RunSystem ( "D:/Programs/KiCad/bin/kicad.exe" )

  def KiCad ( self ) :
    RunSystem ( "D:/Programs/KiCad/bin/kicad.exe" )

  def Heidi ( self ) :
    RunSystem ( "D:/MariaDB/10.3/bin/heidi.bat" )

  def AWS ( self ) :
    RunSystem ( "D:/MariaDB/10.3/bin/mysql.exe -h sql.actions.com.tw -u foxman --password=la0marina" )

  def Local ( self ) :
    RunSystem ( "D:/MariaDB/10.3/bin/mysql.exe -h 192.168.0.98 -u foxman --password=la0marina" )

  def BackupSQL ( self ) :
    RunSystem ( "D:/MariaDB/10.3/bin/mysql.exe -h 192.168.0.97 -u foxman --password=la0marina" )

  def MSYS ( self ) :
    os . system ( "D:/MSYS/msys.bat -norxvt" )

  def MinGW ( self ) :
    RunSystem ( "D:/MSYS/mingw/libexec/mingw-get/guimain.exe" )

  def qtCreator ( self ) :
    RunSystem ( "D:/Qt/Tools/QtCreator/bin/qtcreator.exe" )


def main():
  app = QApplication(sys.argv)

  w = QWidget()
  trayIcon = SystemTrayIcon(QIcon(ActualFile("images/64x64/Menu.png")), w)

  trayIcon.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
