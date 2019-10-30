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
from   CIOS . Voice . VAD        import SplitVoiceByWords

SHOW     = False
Input    = ""
Middle   = ""
Output   = ""
Subtitle = ""
Silence  = 2500
Thresh   = -16

def SayHelp ( ) :
  print ( "SplitByWords.py"
          " -v (--help Help)"
          " -i (--input VideoFile)"
          " -m (--middle AudioFile)"
          " -o (--output ChunkFile)"
          " -t (--thresh Thresh DB)"
          " -e (--silence Silence Length)"
          " -c (--subtitle Subtitle)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Input
  global Middle
  global Output
  global Subtitle
  global Silence
  global Thresh
  try :
    opts, args = getopt . getopt    (
                   argv             ,
                   "i:o:m:t:e:c:sv" ,
                   [ "input="       ,
                     "middle="      ,
                     "output="      ,
                     "subtitle="    ,
                     "thresh="      ,
                     "silence="     ,
                     "show"         ,
                     "help"       ] )
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
    elif opt in ("-m", "--middle"):
      Middle  = arg
    elif opt in ("-o", "--output"):
      Output  = arg
    elif opt in ("-c", "--subtitle"):
      Subtitle  = arg
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
  if ( len ( Middle ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Output ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Subtitle ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  Settings = { "silence" : Silence , "thresh"  : Thresh }
  CMD = f"""ffmpeg -i \"{Input}\" -q:a 0 -map a -acodec pcm_s16le -ac 2 \"{Middle}\""""
  if ( SHOW ) :
    print ( CMD )
  os . system ( CMD )
  Final = SplitVoiceByWords ( Middle , Output , Settings )
  if ( SHOW ) :
    print ( "Split into " , Final )
  R = Recognizer ( )
  i = 1
  Lines =  [ ]
  while ( i <= Final ) :
    out_file = "{0}-{1}.wav" . format ( Output , i )
    R . OpenFile ( out_file )
    line = R . Listen ( )
    if ( len ( line ) > 0 ) :
      t      = int ( i *  5 )
      ss     = int ( t % 60 )
      if ( ss < 10 ) :
        ss = f"0{ss}"
      else :
        ss = f"{ss}"
      t      = int ( t / 60 )
      mm     = int ( t % 60 )
      if ( mm < 10 ) :
        mm = f"0{mm}"
      else :
        mm = f"{mm}"
      tt     = int ( t / 60 )
      STARTS = f"{tt}:{mm}:{ss}"
      e      = int ( ( i + 1 ) * 5 )
      ss     = int ( e % 60 )
      if ( ss < 10 ) :
        ss = f"0{ss}"
      else :
        ss = f"{ss}"
      e      = int ( e / 60 )
      mm     = int ( e % 60 )
      if ( mm < 10 ) :
        mm = f"0{mm}"
      else :
        mm = f"{mm}"
      tt     = int ( e / 60 )
      ENDTS  = f"{tt}:{mm}:{ss}"
      Dialogue = f"Dialogue: 0,{STARTS},{ENDTS},Default,,0,0,0,,{line}"
      Lines . append ( Dialogue )
      if ( SHOW ) :
        print ( Dialogue )
    i = i + 1
  TEXT = "\r\n" . join ( Lines )
  with open ( Subtitle , "w" ) as voiceFile :
    if ( SHOW ) :
      print ( "Writing ... " ,Subtitle  )
    voiceFile . write ( TEXT )
  #
