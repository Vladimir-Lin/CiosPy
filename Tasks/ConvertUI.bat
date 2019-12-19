D:
cd \CIOS\CiosPy\Tasks

python -m PyQt5.uic.pyuic -x TasksMain.ui -o TasksMain.py
pyrcc5 -o TasksResources.py Tasks.qrc
