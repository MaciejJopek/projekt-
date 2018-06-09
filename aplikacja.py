import sys,time
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal,QSize, Qt
from PyQt5.QtGui import *
from random import randint
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
#from czujniki import Sensory
from w1thermsensor import W1ThermSensor


GPIO_TRIGGER = 7 
GPIO_ECHO = 22
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(GPIO_ECHO, GPIO.IN)




class Robot(QWidget):
    trigger = pyqtSignal()
    trigger2 = pyqtSignal()
    def __init__(self,parent=None):
        
        super(Robot,self).__init__(parent)
        GPIO.output(13,1)
        self.p1 = GPIO.PWM(11, 100) #prawy,przod
        self.p2 = GPIO.PWM(18, 100) #lewy przod
        self.p3 = GPIO.PWM(12, 100) #prawy tyl
        self.p4 = GPIO.PWM(16, 100) #lewy tyl
        #self.sensory=Sensory()
        self.plik_temperatura = open('plik_temperatura', 'w')
        self.interfejs()
    def interfejs(self):
        self.zgoda=0
        self.setWindowTitle("Robot")#tytuł okna
        self.setGeometry(50,50,500,300)

        etykieta1 = QLabel("Odleglosc od przeszkody:", self)
        etykieta1.move(300, 50) 
        #przyciski
        self.wynikEdt = QLineEdit(self)
        self.wynikEdt.move(300, 80)
        self.wynikEdt.readonly = True
        etykieta2 = QLabel("Tepmperatura otoczenia:", self)
        etykieta2.move(300, 130)
        self.wynikEdt2 = QLineEdit(self)
        self.wynikEdt2.move(300, 160)
        self.wynikEdt2.readonly = True

        reczne=QRadioButton("Sterowanie reczne",self)
        reczne.move(10,10)
        reczne.setChecked(True)
      
        automatyczne=QRadioButton("Sterowanie automatyczne",self)
        automatyczne.move(180,10)
        
        Wyjscie = QPushButton("Wyjscie",self)
        Wyjscie.move(400,10)
        
        przod = QPushButton("przod",self)
        przod.move(100,120)

        hamulec = QPushButton("hamulec",self)
        hamulec.move(100,170)

        tyl = QPushButton("tyl",self)
        tyl.move(100,222)

        prawo = QPushButton("prawo",self)
        prawo.move(190,170)

        lewo = QPushButton("lewo",self)
        lewo.move(10,170)
        
        etykieta3 = QLabel("Moc silnikow:", self)
        etykieta3.move(10, 50)
        self.suwak = QSlider(Qt.Horizontal)
        self.suwak.setMinimum(0)
        self.suwak.setMaximum(100)
        self.lcd = QLCDNumber()
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        # układ poziomy (splitter) dla slajdera i lcd
        ukladH2 = QSplitter(Qt.Horizontal, self)
        ukladH2.addWidget(self.suwak)
        ukladH2.addWidget(self.lcd)
        ukladH2.setSizes((300, 100))

        ukladH2.move(10,80)

        self.suwak.valueChanged.connect(self.lcd.display)
        self.suwak.valueChanged.connect(self.predkosc)
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
        self.shortcut.activated.connect(self.silnik_przod)
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
    def predkosc(self):
        self.predkosc = self.suwak.value()
    def reczne(self):
        self.zgoda=0
        self.hamulec()   
    def automatyczne(self):
        self.zgoda=1
    def odleglosc(self,val):
        if (val<200):
            self.wynikEdt.setText(str(val))
        if (val>200):
            self.wynikEdt.setText('ponad 2 metry')
        if (self.zgoda==1):
            if (val>40):
                self.x=2
                self.silnik_przod()               
            if (val<40):
                if self.x==2:
                    self.losowanie_zgoda=9
                if self.x>1:
                    self.losowanie_zgoda=5
                    if self.losowanie_zgoda==5:
                        self.x=randint(0,1)
                if (self.x==0):
                    self.lewy()
                if (self.x==1):
                    self.prawy()
                time.sleep(0.1)  
    def termometr(self,temperatura):
        self.wynikEdt2.setText(str(temperatura))
        print(temperatura, file=self.plik_temperatura)
    def przod(self,val):
        self.silnik_przod()
    def hamulec(self):
        self.hamulec_2()
    def tyl(self):
        self.silnik_tyl()
    def lewo(self):
        self.lewy()
    def prawo(self):
        self.prawy()
    def silnik_przod(self):
        self.p3.stop()
        self.p4.stop()
        self.p1.start(self.predkosc)
        self.p2.start(self.predkosc+5)
    def silnik_tyl(self):
        self.p1.stop()
        self.p2.stop()
        self.p3.start(self.predkosc)
        self.p4.start(self.predkosc+5)
            
    def hamulec_2(self):

        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()

            
    def prawy(self):
        self.p1.stop()
        self.p3.stop()
        self.p4.stop()
        self.p2.start(self.predkosc+5)

    def lewy(self):
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        self.p1.start(self.predkosc)
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
            time.sleep(0.5)
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
            self.val = TimeElapsed * 17150
            self.progress_update.emit(self.val)
            
class Threadclass2(QtCore.QThread):
    progress_update2 = pyqtSignal(float)
    def __init__(self,parent = None):
        super(Threadclass2,self).__init__(parent)
    def run(self):
        sensor = W1ThermSensor()

        while True:  
            self.temperatura = float(sensor.get_temperature())

            self.progress_update2.emit(self.temperatura)

            time.sleep(2)


if __name__ == '__main__':
    app=QApplication(sys.argv)#obiekt reprezentujacy aplikacje
    okno=Robot()#obiekt reprezentujacy okno aplikacji
    sys.exit(app.exec_())#app.exec_() głowna pętla programu
