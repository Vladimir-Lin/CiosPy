import os
import sys
import mysql.connector

myname = "name.txt"
subtitle = "subtitles.ass"

if not os.path.exists(myname):
  print ( "file '" + myname + "' is missing" )
  sys.exit(0)

namefile = open("name.txt","r+")
lines = namefile.readlines()
namefile.close()

videoname = lines [ 0 ]

if ( len(videoname) <= 0 ) :
  print ( myname + " does not contain video name" )
  sys.exit(0)

pypath = os.path.dirname(os.path.abspath(__file__))
pypath = os.path.abspath(os.path.join(pypath,".."))

enass = os.path.abspath(os.path.join(pypath,"subtitles","EN",subtitle))
twass = os.path.abspath(os.path.join(pypath,"subtitles","TW",subtitle))
cnass = os.path.abspath(os.path.join(pypath,"subtitles","CN",subtitle))
jpass = os.path.abspath(os.path.join(pypath,"subtitles","JP",subtitle))

if os.path.exists(twass):
  os.remove(twass)

if os.path.exists(cnass):
  os.remove(cnass)

if os.path.exists(jpass):
  os.remove(jpass)

cmds = "copy \"" + enass + "\" \"" + twass + "\""
print ( cmds )
os.system ( cmds )

cmds = "copy \"" + enass + "\" \"" + cnass + "\""
print ( cmds )
os.system ( cmds )

cmds = "copy \"" + enass + "\" \"" + jpass + "\""
print ( cmds )
os.system ( cmds )
