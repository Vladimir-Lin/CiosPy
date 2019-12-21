D:
cd \CIOS\CiosPy\Pictures

python -m PyQt5.uic.pyuic -x PicturesMain.ui -o PicturesMain.py
pyrcc5 -o Resources.py Pictures.qrc
