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
Output  = "Cover.mp4"
Audio   = "Cover.mp3"
Silence = "Silence.mp3"

def SayHelp ( ) :
  print ( "ExtractHeadingClip.py"
          " -v (--help Help)"
          " -i (--input VideoFile)"
          " -o (--output VideoFile)"
          " -a (--audio AudioFile)"
          " -e (--silence EmptyAudioFile)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Source
  global Output
  global Audio
  global Silence
  try :
    opts, args = getopt.getopt(argv,"i:o:a:e:sv",["input=","output=","audio=","silence=","show","help"])
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
    elif opt in ("-o", "--output"):
      Output  = arg
    elif opt in ("-a", "--audio"):
      Audio   = arg
    elif opt in ("-e", "--silence"):
      Audio   = arg
  return True

def ExtractHeading ( ) :
  global SHOW
  global Source
  global Output
  global Audio
  global Silence
  cwdir = os . getcwd ( )
  if os . path . isfile ( Output ) :
    os . remove ( Output )
  if os . path . isfile ( Audio ) :
    os . remove ( Audio )
  if os . path . isfile ( Silence ) :
    os . remove ( Silence )
  CMD = f"""ffmpeg -i \"{Source}\" -ss 00:00:00 -t 00:00:07 -async 1 -strict -2 \"{Output}\""""
  os . system ( CMD )
  CMD = f"""ffmpeg -i \"{Output}\" -q:a 0 -map a \"{Audio}\""""
  os . system ( CMD )
  os . chdir  ( cwdir )
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( len ( Source ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Output ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  ExtractHeading ( )
