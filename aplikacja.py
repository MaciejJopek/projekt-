from time import sleep
import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
import sys
from czujniki import Sensory
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
class Robot(QWidget,Sensory):
    def __init__(self,parent=None):

        super(Robot,self).__init__(parent)

        self.sensory=Sensory()
        self.interfejs()
    def interfejs(self):
        self.setWindowTitle("Robot")#tytuł okna
        self.setGeometry(50,50,600,500)
        #przyciski
        reczne=QRadioButton("Sterowanie reczne",self)
        reczne.move(10,10)
        reczne.setChecked(True)
      
        automatyczne=QRadioButton("Sterowanie automatyczne",self)
        automatyczne.move(180,10)

        Start = QPushButton("Start",self)
        Start.move(10,50)
        
        Stop = QPushButton("Stop",self)
        Stop.move(100,50)
        
        Wyjscie = QPushButton("Wyjscie",self)
        Wyjscie.move(450,10)
        
        przod = QPushButton("przod",self)
        przod.move(100,100)

        hamulec = QPushButton("hamulec",self)
        hamulec.move(100,150)

        tyl = QPushButton("tyl",self)
        tyl.move(100,200)

        prawo = QPushButton("prawo",self)
        prawo.move(190,150)

        lewo = QPushButton("lewo",self)
        lewo.move(10,150)

        Start.clicked.connect(self.Start)
        Stop.clicked.connect(self.Stop)
        Wyjscie.clicked.connect(self.Wyjscie)
        reczne.clicked.connect(self.reczne)
        automatyczne.clicked.connect(self.automatyczne)
        przod.clicked.connect(self.przod)
        hamulec.clicked.connect(self.hamulec)
        tyl.clicked.connect(self.tyl)
        prawo.clicked.connect(self.prawo)
        lewo.clicked.connect(self.lewo)

        self.show()#wyswietla okno na ekranie

    @pyqtSlot()    
    def Start(self):
        self.sensory.start()
    def Stop(self):       
        self.sensory.stop()
    def reczne(self):
        self.sensory.reczne_sterowanie()
    def automatyczne(self):
        self.sensory.automatyczne_sterowanie()
    def przod(self):
        self.sensory.silnik_przod()
    def hamulec(self):
        self.sensory.hamulec()
    def tyl(self):
        self.sensory.silnik_tyl()
    def lewo(self):
        self.sensory.lewy()
    def prawo(self):
        self.sensory.prawy()
    def Wyjscie(self):
        GPIO.cleanup()
        self.close()    
class aplikacja(object):
    def __init__(self):
        app=QApplication(sys.argv)#obiekt reprezentujacy aplikacje
        okno=Robot()#obiekt reprezentujacy okno aplikacji
        sys.exit(app.exec_())#app.exec_() głowna pętla programu
