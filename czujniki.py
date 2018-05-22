import RPi.GPIO as GPIO
class Sensory(object):
    def __init__(self,parent=None):
        GPIO.output(13,1)
        self.p1 = GPIO.PWM(11, 100) #prawy,przod
        self.p2 = GPIO.PWM(18, 100) #lewy przod
        self.p3 = GPIO.PWM(12, 100) #prawy tyl
        self.p4 = GPIO.PWM(16, 100) #lewy tyl
    def silnik_przod(self):
        print ("jedzie do przodu")
        self.p3.stop()
        self.p4.stop()
        self.p1.start(70)
        self.p2.start(75)
    def silnik_tyl(self):
        print ("jedzie do tylu")
        self.p1.stop()
        self.p2.stop()
        self.p3.start(70)
        self.p4.start(75)
            
    def hamulec(self):
        print ("hamulec dziala")
        #GPIO.output(11, GPIO.LOW)
        self.p1.stop()
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        #GPIO.output(18, GPIO.LOW)
            
    def prawy(self):
        self.p1.stop()
        self.p3.stop()
        self.p4.stop()
        self.p2.start(75)

    def lewy(self):
        self.p2.stop()
        self.p3.stop()
        self.p4.stop()
        self.p1.start(70)

        
        
