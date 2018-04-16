import RPi.GPIO as GPIO
class Sensory(object):       
    def __init__(self):
        self.wlaczony=0
    def start(self):
        self.wlaczony=1
        GPIO.output(15, 1)
        GPIO.output(13, 0)
    def stop(self):       
        self.wlaczony=0;
        GPIO.output(15, 0)
        GPIO.output(13, 1)
     
    def silnik_przod(self):
        print ("jedzie do przodu")
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
    def silnik_tyl(self):
        print ("jedzie do tylu")
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
            
    def hamulec(self):
        print ("hamulec dziala")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
            
    def prawy(self):

        GPIO.output(11, GPIO.HIGH)

    def lewy(self):
        GPIO.output(18, GPIO.HIGH)

        
        
