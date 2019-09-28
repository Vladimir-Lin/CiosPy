SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.bat

include ($${PWD}/images/images.pri)
include ($${PWD}/projects/projects.pri)
include ($${PWD}/roles/roles.pri)
include ($${PWD}/scripts/scripts.pri)
include ($${PWD}/subtitles/subtitles.pri)
include ($${PWD}/videos/videos.pri)
