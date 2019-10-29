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

R = Recognizer ( )
# R . OpenMicrophone (   )
# R . OpenMicrophone ( Device = 1 )
# R . OpenMicrophone ( Device = 7 )

# R . OpenFile ( "trying.wav" )
# print ( R . Listen ( ) )

while True :
  R . OpenMicrophone ( Device = 1 )
  R . UseMicrophone ( )
  print ( R . Listen ( ) )







# import speech_recognition as vrt

# rtx = vrt . Recognizer ( )

# mic = vrt . Microphone ( )
# mic = vrt . Microphone ( device_index = 1 )
# mic = vrt . Microphone ( device_index = 7 )

# print ( vrt . Microphone . list_microphone_names ( ) )

# hasSource = False

# harvard = vrt . AudioFile ( 'trying.wav' )
# with harvard as source:
#   audio = rtx . record ( source )
#   hasSource = True

# with mic as source :
#   audio = rtx . listen ( source )
#   hasSource = True

# if ( hasSource ) :
  # print ( rtx . recognize_sphinx ( audio ) )
#   print ( rtx . recognize_google ( audio ) )
  # -- okay, google is good
  # print ( rtx . recognize_google_cloud ( audio ) )
  # print ( rtx . recognize_bing ( audio ) ) -- 需要key
  # print ( rtx . recognize_houndify ( audio ) ) 需要client_id及client_key
  # print ( rtx . recognize_ibm ( audio ) ) -- 需要帳戶密碼
  # print ( rtx . recognize_wit ( audio ) ) -- 需要key
# else :
#   print ( "No source" )
