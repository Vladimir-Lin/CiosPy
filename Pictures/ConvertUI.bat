D:
cd \CIOS\CiosPy\People

python -m PyQt5.uic.pyuic -x PeopleMain.ui -o PeopleMain.py
pyrcc5 -o Resources.py People.qrc
