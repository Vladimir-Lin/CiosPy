import os
import sys
import getopt
import time
import requests
import threading
import mysql.connector
from mysql.connector import Error
import Actions
import CIOS
from multiprocessing import Process

time . sleep ( 2 )
CiosPy = os . path . dirname ( os . path . abspath (__file__) ) + "/CiosPy.py"
os . system ( "start pythonw " + CiosPy )
