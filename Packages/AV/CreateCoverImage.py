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

cwdir   = os . getcwd ( )
left    = ""
right   = ""

for root , dirs , files in os . walk ( cwdir ) :
  for file in files:
    if   file . endswith ( "bh.jpg" ) :
      left  = file
    elif file . endswith (  "h.jpg" ) :
      right = file

cmd = "magick.exe " + left + " " + right + " +append Cover.jpg"
os . system ( cmd )
