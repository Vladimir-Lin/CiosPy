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
from   CIOS . Voice . Recognizer import Recognizer

FromSource = "File"
AudioFile  = ""
OutputFile = ""
Language   = "en-US"

def SayHelp ( ) :
  print ( "VoiceRecognition.py"
          " -v (--help Help)"
          " -f (--from MIC or File)"
          " -i (--input AudioFile)"
          " -o (--output OutputFile)"
          " -l (--language Language)"
          )

def GetOptions ( argv ) :
  global FromSource
  global AudioFile
  global OutputFile
  global Language
  try :
    opts, args = getopt . getopt (
                   argv          ,
                   "i:o:f:l:v"   ,
                   [ "input="    ,
                     "output="   ,
                     "language=" ,
                     "from="     ,
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
    elif opt in ("-o", "--output"):
      OutputFile = arg
    elif opt in ("-l", "--language"):
      Language   = arg
    elif opt in ("-f", "--from"):
      FromSource  = arg
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( FromSource ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( "File" == FromSource ) :
    if ( len ( AudioFile ) <= 0 ) :
      SayHelp ( )
      sys . exit ( 2 )
  R = Recognizer ( )
  if ( "MIC" == FromSource ) :
    R . OpenMicrophone ( Device = 1 )
    Running = True
    while Running :
      R . UseMicrophone ( )
      line = R . Listen ( Language )
      if ( len ( line ) > 0 ) :
        print ( line )
        line = line . strip ( )
        line = line . lower ( )
        if ( line == "stop" ) :
          Running = False
    print ( "Program stopped" )
  else :
    R . OpenFile ( AudioFile )
    line = R . Listen ( Language )
    print ( line )
    if ( len ( OutputFile ) > 0 ) :
      if ( len ( line ) > 0 ) :
        with open ( OutputFile , "w" ) as voiceFile :
          voiceFile . write ( line )
