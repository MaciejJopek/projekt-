import sys,time
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal,QSize
from PyQt5.QtGui import *
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
from czujniki import Sensory
from w1thermsensor import W1ThermSensor


GPIO_TRIGGER = 7 
GPIO_ECHO = 22
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(GPIO_ECHO, GPIO.IN)




class Robot(QWidget,Sensory):
    trigger = pyqtSignal()
    trigger2 = pyqtSignal()
    def __init__(self,parent=None):
        
        super(Robot,self).__init__(parent)
        self.sensory=Sensory()
        self.plik_temperatura = open('plik_temperatura', 'w')
        self.interfejs()
    def interfejs(self):
        self.zgoda=0
        self.setWindowTitle("Robot")#tytuł okna
        self.setGeometry(50,50,600,500)
        #przyciski
        self.wynikEdt = QLineEdit(self)
        self.wynikEdt.move(300, 150)
        self.wynikEdt.readonly = True

        self.wynikEdt2 = QLineEdit(self)
        self.wynikEdt2.move(300, 200)
        self.wynikEdt2.readonly = True

        reczne=QRadioButton("Sterowanie reczne",self)
        reczne.move(10,10)
        reczne.setChecked(True)
      
        automatyczne=QRadioButton("Sterowanie automatyczne",self)
        automatyczne.move(180,10)
        
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
        
        #czujnik odleglosci
        self.threadclass= Threadclass()
        self.threadclass.start()
        self.threadclass.progress_update.connect(self.odleglosc)

        #czujnik temperatury
        self.threadclass2= Threadclass2()
        self.threadclass2.start()
        self.threadclass2.progress_update2.connect(self.termometr)
        

        Wyjscie.clicked.connect(self.Wyjscie)
        reczne.clicked.connect(self.reczne)
        automatyczne.clicked.connect(self.automatyczne)
        przod.clicked.connect(self.przod)
        hamulec.clicked.connect(self.hamulec)
        tyl.clicked.connect(self.tyl)
        prawo.clicked.connect(self.prawo)
        lewo.clicked.connect(self.lewo)

        #sterowanie klawiatura
        self.shortcut = QShortcut(QKeySequence("w"),self)
        self.shortcut.activated.connect(self.przod)
        self.shortcut = QShortcut(QKeySequence("a"),self)
        self.shortcut.activated.connect(self.lewo)
        self.shortcut = QShortcut(QKeySequence("d"),self)
        self.shortcut.activated.connect(self.prawo)
        self.shortcut = QShortcut(QKeySequence("s"),self)
        self.shortcut.activated.connect(self.tyl)
        self.shortcut = QShortcut(QKeySequence(" "),self)
        self.shortcut.activated.connect(self.hamulec)
        self.show()#wyswietla okno na ekranie

    @pyqtSlot()    
    def reczne(self):
        self.zgoda=0
        self.sensory.hamulec()   
    def automatyczne(self):
        self.zgoda=1
    def odleglosc(self,val):
        if (val<200):
            self.wynikEdt.setText(str(val))
        if (val>200):
            self.wynikEdt.setText('ponad 2 metry')
        if (self.zgoda==1):
            if (val>40):
                self.sensory.silnik_przod()               
            else:
                self.sensory.lewy()
                time.sleep(0.1)
    def termometr(self,temperatura):
        self.wynikEdt2.setText(str(temperatura))
        print(temperatura, file=self.plik_temperatura)
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
        self.plik_temperatura.close()
        GPIO.cleanup()
        self.close()
class Threadclass(QtCore.QThread):
    progress_update = pyqtSignal(int)
    def __init__(self,parent = None):
        super(Threadclass,self).__init__(parent)
    def run(self):
        while True:
            time.sleep(0.4)
            GPIO.output(7, True)
            
            time.sleep(0.00001)

            GPIO.output(7, False)

            poczatek = time.time()

            koniec= time.time()

            while GPIO.input(22) == 0:

                StartTime = time.time()

            while GPIO.input(22) == 1:
                koniec = time.time()
            TimeElapsed = koniec - poczatek
            val = TimeElapsed * 17150
            self.progress_update.emit(val)
            
class Threadclass2(QtCore.QThread):
    progress_update2 = pyqtSignal(float)
    def __init__(self,parent = None):
        super(Threadclass2,self).__init__(parent)
    def run(self):
        sensor = W1ThermSensor()
        #temp=[]
        #x=0
        while True:  
            temperatura = float(sensor.get_temperature())
            #temp.append(temperatura)
            #x=x+1
            #if (x>10):
                #temp.pop(0)
            self.progress_update2.emit(temperatura)

            time.sleep(1)


if __name__ == '__main__':
    app=QApplication(sys.argv)#obiekt reprezentujacy aplikacje
    okno=Robot()#obiekt reprezentujacy okno aplikacji
    sys.exit(app.exec_())#app.exec_() głowna pętla programu
