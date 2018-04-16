import sys,time
import RPi.GPIO as GPIO
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal,QSize
from czujniki import Sensory
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
#set GPIO Pins
GPIO_TRIGGER = 7 
GPIO_ECHO = 22
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(GPIO_ECHO, GPIO.IN)

class Robot(QWidget,Sensory):
    trigger = pyqtSignal()
    def __init__(self,parent=None):

        super(Robot,self).__init__(parent)
        self.zgoda=0
        self.sensory=Sensory()
        self.interfejs()
    def interfejs(self):
        self.setWindowTitle("Robot")#tytuł okna
        self.setGeometry(50,50,600,500)
        #przyciski
        self.wynikEdt = QLineEdit(self)
        self.wynikEdt.move(300, 150)
        self.wynikEdt.readonly = True

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

        self.threadclass= Threadclass()
        self.threadclass.start()
        self.threadclass.progress_update.connect(self.zaczynamy_odliczanie)
        
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
        self.sensory.hamulec()
        self.zgoda=0    
    def automatyczne(self):
        self.zgoda=1
    def zaczynamy_odliczanie(self,val): 
        self.wynikEdt.setText(str(val))
        if (self.zgoda==1):
            if (val>20):
                self.sensory.silnik_przod()
            else:
                self.sensory.hamulec()
            
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
class Threadclass(QtCore.QThread):
    progress_update = pyqtSignal(int)
    def __init__(self,parent = None):
        super(Threadclass,self).__init__(parent)
    def run(self):
        while True:

            GPIO.output(7, True)
            
            time.sleep(0.00001)

            GPIO.output(7, False)

            StartTime = time.time()

            StopTime = time.time()

            while GPIO.input(22) == 0:

                StartTime = time.time()

            while GPIO.input(22) == 1:
                StopTime = time.time()
            TimeElapsed = StopTime - StartTime
            val = (TimeElapsed * 34300) / 2
 

            #print ("Measured Distance = %.1f cm" % val)
            self.progress_update.emit(val)
            time.sleep(1.5)

if __name__ == '__main__':
    app=QApplication(sys.argv)#obiekt reprezentujacy aplikacje
    okno=Robot()#obiekt reprezentujacy okno aplikacji
    sys.exit(app.exec_())#app.exec_() głowna pętla programu
