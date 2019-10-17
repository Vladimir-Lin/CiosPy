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

rootdir = os . path . dirname ( os . path . abspath ( __file__ ) )
rootdir = rootdir + "/../../Templates/AV/Folder" ;
rootdir = os . path . abspath ( rootdir )
cwdir   = os . getcwd ( )

for i in range ( 1 , len ( sys . argv ) ) :
  name   = sys . argv [ i ]
  dname  = cwdir + "/" + name
  fname  = dname + "/scripts/name.txt"
  shutil . copytree ( rootdir , dname         )
  f      = open     ( fname   , 'wb'          )
  f      . write    ( name . encode ( "utf8") )
  f      . close    (                         )
