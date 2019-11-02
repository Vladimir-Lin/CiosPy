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
from   playsound import playsound

AudioFile = ""

def SayHelp ( ) :
  print ( "PlaySound.py"
          " -v (--help Help)"
          " -i (--input AudioFile)"
          )

def GetOptions ( argv ) :
  global FromSource
  global AudioFile
  global OutputFile
  global Language
  try :
    opts, args = getopt . getopt (
                   argv          ,
                   "i:v"   ,
                   [ "input="    ,
                     "help"    ] )
  except getopt . GetoptError :
    SayHelp ( )
    sys . exit ( 2 )
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-i", "--input"):
      AudioFile  = arg
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( AudioFile ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  playsound ( AudioFile )
