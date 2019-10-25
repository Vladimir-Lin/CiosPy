# -*- coding: utf-8 -*-
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import shutil
import mysql.connector
from mysql.connector import Error
import Actions
import CIOS

SHOW   = False
Walk   = False

def SayHelp ( ) :
  print ( "GenerateAlbum.py"
          " -v (--help Help)"
          " -w --walk (Walk throught the entire directory)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Walk
  try :
    opts, args = getopt.getopt(argv,"wsv",["walk","show","help"])
  except getopt.GetoptError:
    SayHelp ( )
    sys . exit ( 2 )
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-s", "--show") :
      SHOW    = True
    elif opt in ("-w", "--walk") :
      Walk    = True
  return True

def GenerateAlbum ( ) :
  global SHOW
  Name  = ""
  MyDIR = os . path . dirname ( os . path . abspath (__file__) )
  cwdir = os . getcwd ( )
  with open ( 'scripts/name.txt' , 'r' ) as file :
    data  = file . read ( )
    lines = data . split ( "\n" )
    Name  = lines [ 0 ]
    Name  = Name . strip ( )
  if ( len ( Name ) <= 0 ) :
    return False
  os . chdir ( "videos" )
  CMD = f"{MyDIR}/ProbeImageDimension.py -i \"{Name}.mp4\""
  os . system ( CMD )
  CMD = f"{MyDIR}/ExtractHeadingClip.py -i \"{Name}.mp4\""
  os . system ( CMD )
  os . chdir  ( cwdir )
  os . chdir  ( "images" )
  CMD = f"{MyDIR}/CreateCoverImage.py"
  os . system ( CMD )
  CMD = f"{MyDIR}/CreateHeadingImage.py --probe"
  os . system ( CMD )
  os . chdir ( cwdir )
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( Walk ) :
    cwdir = os . getcwd ( )
    for root , dirs , files in os . walk ( "." ) :
      for d in dirs :
        print ( d )
        os . chdir ( d )
        GenerateAlbum ( )
        os . chdir ( cwdir )
      break
    os . chdir ( cwdir )
  else :
    GenerateAlbum ( )
