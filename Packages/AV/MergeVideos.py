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

SHOW    = False
Source  = ""
Input   = [ ]
Output  = "Cover.mp4"

def SayHelp ( ) :
  print ( "MergeVideos.py"
          " -v (--help Help)"
          " -o (--output VideoFile)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Input
  global Output
  try :
    opts, args = getopt.getopt(argv,"o:sv",["output=","show","help"])
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
    elif opt in ("-o", "--output"):
      Output  = arg
  return True

def MergeVideos ( ) :
  global SHOW
  global Input
  global Output
  cwdir = os . getcwd ( )
  FILES = [ ]
  for i in Input :
    x = i
    x = x . replace ( "\r" , "" )
    x = x . replace ( "\n" , "" )
    FILES . append ( f"file {i}" )
  TEXT = "\r\n" . join ( FILES )
  with open ( "video-list.txt" , "w" , encoding="utf-8" ) as file :
    file . write ( TEXT )
  CMD = f"ffmpeg -f concat -safe 0 -i video-list.txt -vcodec libx264 -crf 18 -acodec aac -ab 128k -ar 48000 {Output}"
  os . system ( CMD   )
  os . chdir  ( cwdir )
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( Input ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Output ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  MergeVideos ( )
