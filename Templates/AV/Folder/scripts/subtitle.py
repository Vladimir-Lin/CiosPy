import os
import sys
import mysql.connector

ffmpeg = "ffmpeg.exe"
myname = "name.txt"
metadata = "metadata.txt"
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

videofile = videoname + ".mp4"
videofile = os.path.abspath(os.path.join(pypath,"videos",videofile))
videonew = videoname + "-Subtitles.mp4"
videonew = os.path.abspath(os.path.join(pypath,"videos",videonew))

if not os.path.exists(videofile):
  print ( "video '" + videofile + "' does not exist" )
  sys.exit(0)

metafile = os.path.abspath(os.path.join(pypath,"scripts",metadata))

if not os.path.exists(metafile):
  os.system ( "python chapter.py" )

enass = os.path.abspath(os.path.join(pypath,"subtitles","EN",subtitle))
twass = os.path.abspath(os.path.join(pypath,"subtitles","TW",subtitle))
cnass = os.path.abspath(os.path.join(pypath,"subtitles","CN",subtitle))
jpass = os.path.abspath(os.path.join(pypath,"subtitles","JP",subtitle))

# 移除簡體中文

if os.path.exists(cnass):
  os.remove(cnass)

# 複製繁體中文到簡體中文

cmds = "copy \"" + twass + "\" \"" + cnass + "\""
os.system ( cmds )

# 繁簡互換

os.chdir(os.path.abspath(os.path.join(pypath,"subtitles","CN")))
os.system ( "TW2CN.exe --suffix ass --files " + subtitle )

# 執行字幕合併

os.chdir(pypath)

cmds = ffmpeg + " -i "
cmds = cmds + "\"" + videofile + "\""
cmds = cmds + " -i "
cmds = cmds + "\"" + metafile + "\""
cmds = cmds + " -i "
cmds = cmds + "\"" + enass + "\""
cmds = cmds + " -i "
cmds = cmds + "\"" + twass + "\""
cmds = cmds + " -i "
cmds = cmds + "\"" + cnass + "\""
cmds = cmds + " -i "
cmds = cmds + "\"" + jpass + "\""
cmds = cmds + " -c copy -map_metadata 1 -map 0:v -map 0:a "
cmds = cmds + "-map 2 -c:s mov_text -metadata:s:s:0 language=eng "
cmds = cmds + "-map 3 -c:s mov_text -metadata:s:s:1 language=zht "
cmds = cmds + "-map 4 -c:s mov_text -metadata:s:s:2 language=zhs "
cmds = cmds + "-map 5 -c:s mov_text -metadata:s:s:3 language=jp "
cmds = cmds + "-metadata title=\"" + videoname + "\""
cmds = cmds + " -y \"" + videonew + "\""

rv = os.system ( cmds )

# if rv == 0 :
#   print ( "success" )

