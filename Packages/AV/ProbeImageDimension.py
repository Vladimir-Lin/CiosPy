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
Source = ""

def SayHelp ( ) :
  print ( "ProbeImageDimension.py"
          " -v (--help Help)"
          " -i (--input VideoFile)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Source
  try :
    opts, args = getopt.getopt(argv,"i:sv",["input=","show","help"])
  except getopt.GetoptError:
    SayHelp ( )
    sys . exit ( 2 )
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-s", "--show") :
      SHOW    = True
    elif opt in ("-i", "--input"):
      Source  = arg
  return True

def ProbeDimension ( ) :
  global SHOW
  global Source
  cwdir = os . getcwd ( )
  Target = os . path . abspath ( "../scripts/dimension.txt" )
  cmd   = f"""ffprobe.exe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1:nk=1 \"{Source}\" > \"{Target}\""""
  os . system ( cmd )
  os . chdir ( cwdir )
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( Source ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  ProbeDimension ( )
