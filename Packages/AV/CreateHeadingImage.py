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
from wand.api import library
from wand.image import Image
from wand.color import Color
from wand.compat import nested
import Actions
import CIOS

SHOW   = False
Probe  = False
Width  = 0
Height = 0
Source = "Cover.jpg"
Output = "Heading.png"

def SayHelp ( ) :
  print ( "CreateHeadingImage.py"
          " -v (--help Help)"
          " -p (--probe)"
          " -w Width (--width=Width)"
          " -h Height (--height=Height)"
          " -i Input (--input=Input)"
          " -o Output (--output=Output)"
          " -s --show(Show message)" )

def GetOptions ( argv ) :
  global SHOW
  global Probe
  global Width
  global Height
  global Source
  global Output
  try :
    opts, args = getopt.getopt(argv,"w:h:i:o:psv",["width=","height=","input=","output=","probe","show","help"])
  except getopt.GetoptError:
    SayHelp ( )
    sys . exit ( 2 )
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-s", "--show") :
      SHOW    = True
    elif opt in ("-p", "--probe"):
      Probe   = True
    elif opt in ("-w", "--width"):
      Width   = int ( arg )
    elif opt in ("-h", "--height"):
      Height  = int ( arg )
    elif opt in ("-i", "--input"):
      Source  = arg
    elif opt in ("-o", "--output"):
      Output  = arg
  return True

def resizeImage ( sourceFile , destFile , w , h , color = Color ( "transparent" ) ) :
  with Image ( width = w , height = h , background = color ) as outImg :
    with Image ( filename = sourceFile ) as inpImg :
      inpImg . resize    ( int ( inpImg . width * 2 ) , int ( inpImg . height * 2 ) )
      inpImg . transform ( resize = "%dx%d>" % ( w , h ) )
      outImg . format = inpImg . format . lower ( )
      outImg . composite ( inpImg , left = int ( ( w - inpImg . width ) / 2 ) , top = int ( ( h - inpImg . height ) / 2 ) )
      outImg . save      ( filename = destFile )

def CreateHeading ( ) :
  global SHOW
  global Width
  global Height
  global Source
  global Output
  resizeImage ( Source , Output , Width , Height , Color ( "black" ) )
  return True

if __name__ == '__main__':
  GetOptions ( sys . argv [ 1: ] )
  if ( Probe ) :
    cwdir = os . getcwd ( )
    with open ( '../scripts/dimension.txt' , 'r' ) as file :
      data   = file . read ( )
      lines  = data . split ( "\n" )
      Width  = int ( lines [ 0 ] )
      Height = int ( lines [ 1 ] )
    os . chdir ( cwdir )
  if ( Width <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( Height <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Source ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  if ( len ( Output ) <= 0 ) :
    SayHelp ( )
    sys . exit ( 2 )
  CreateHeading ( )
