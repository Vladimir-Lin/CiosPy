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
from   CIOS . Voice . VAD import SplitVoiceByWords

Input   = ""
Output  = ""
Silence = 1000
Thresh  = -16

def SayHelp ( ) :
  print ( "SplitByWords.py"
          " -v (--help Help)"
          " -i (--input AudioFile)"
          " -o (--output ChunkFile)"
          " -t (--thresh Thresh DB)"
          " -e (--silence Silence Length)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Input
  global Output
  global Silence
  global Thresh
  try :
    opts, args = getopt.getopt(argv,"i:o:t:e:sv",["input=","output=","--thresh","--silence","show","help"])
  except getopt.GetoptError:
    SayHelp ( )
    sys . exit ( 2 )
  Input = args
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-s", "--show") :
      SHOW    = True
    elif opt in ("-i", "--input"):
      Input  = arg
    elif opt in ("-o", "--output"):
      Output  = arg
    elif opt in ("-t", "--thresh"):
      Thresh  = arg
    elif opt in ("-e", "--silence"):
      Silence = arg
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( Input ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Output ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  Settings = { "silence" : Silence , "thresh"  : Thresh }
  SplitVoiceByWords ( Input , Output , Settings )
