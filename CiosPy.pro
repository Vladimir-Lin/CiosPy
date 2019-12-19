SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.bat
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.md

include ($${PWD}/audios/audios.pri)
include ($${PWD}/images/images.pri)
include ($${PWD}/Libs/Libs.pri)
include ($${PWD}/Templates/Templates.pri)
include ($${PWD}/Packages/Packages.pri)
include ($${PWD}/UI/UI.pri)
include ($${PWD}/Tasks/Tasks.pri)
include ($${PWD}/People/People.pri)
