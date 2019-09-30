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
from Actions import *
# import Actions
import CIOS
from CIOS.SQL import SqlQuery
from CIOS.SQL import SqlConnection
from CIOS.Database import Tables

UuidsDB = CiosDB
SHOW    = False

def SayHelp ( ) :
  print ( "CreateTables.py"
          " -v (--help Help)"
          " -h Hostname (--hostname=Hostname)"
          " -u Username (--username=Username)"
          " -p Password (--password=Password)"
          " -d Database (--database=Database)"
          " -s --show(Show message)" )

def GetOptions ( DbSettings , argv ) :
  global SHOW
  try :
    opts, args = getopt.getopt(argv,"h:u:p:d:sv",["hostname=","username=","password=","database=","show","help"])
  except getopt.GetoptError:
    SayHelp ( )
    sys . exit ( 2 )
  for opt, arg in opts:
    if opt in ( "-v" , "--help" ) :
      SayHelp ( )
      sys . exit ( 0 )
    elif opt in ("-s", "--show") :
      SHOW = True
    elif opt in ("-h", "--hostname"):
      DbSettings [ "hostname" ] = arg
    elif opt in ("-u", "--username"):
      DbSettings [ "username" ] = arg
    elif opt in ("-p", "--password"):
      DbSettings [ "password" ] = arg
    elif opt in ("-d", "--database"):
      DbSettings [ "database" ] = arg
  return DbSettings

def CreateTables ( ) :
  global SHOW
  global UuidsDB
  SC      = SqlConnection ( )
  UuidsDB = GetOptions ( UuidsDB , sys . argv [ 1: ] )

  SC . ConnectTo ( UuidsDB )

  if SC . isConnected ( ) :
    if SHOW :
      print ( "Connected to MySQL database " + UuidsDB [ "hostname" ] )
  else :
    if SHOW :
      print ( 'Can not connect to MySQL database' )
    sys . exit ( 0 )

  SC . Prepare ( )
  SC . CreateStructures ( CIOS . Database . Templates . CiosTableStructures )
  SC . Close ( )

if __name__ == '__main__':
  CreateTables ( )
