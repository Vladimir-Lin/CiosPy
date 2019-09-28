import os
import sys
import mysql.connector

#ffmpeg.exe -i "videofile.mp4" -f ffmetadata metadata.txt

ffmpeg = "ffmpeg.exe"
myname = "name.txt"
metadata = "metadata.txt"

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

videofile = videoname + ".mp4"
videofile = os.path.abspath(os.path.join(pypath,"videos",videofile))

if not os.path.exists(videofile):
  print ( "video '" + videofile + "' does not exist" )
  sys.exit(0)

metafile = os.path.abspath(os.path.join(pypath,"scripts",metadata))

if os.path.exists(metafile):
  os.remove(metafile)

cmds = ffmpeg + " -i "
cmds = cmds + "\"" + videofile + "\""
cmds = cmds + " -f ffmetadata "
cmds = cmds + "\"" + metafile + "\""

rv = os.system ( cmds )

# if rv == 0 :
#  print ( "success" )

