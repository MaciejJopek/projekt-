import RPi.GPIO as GPIO
class Sensory(object):       
    def __init__(self):
        self.wlaczony=0
        self.sterowanie=0
    def start(self):
        self.wlaczony=1
        GPIO.output(15, 1)
        GPIO.output(13, 0)
    def stop(self):       
        self.wlaczony=0;
        GPIO.output(15, 0)
        GPIO.output(13, 1)
     
    def silnik_przod(self):
        if (self.sterowanie==1):
            print ("Wybrales sterowanie automatyczne, w celu sterowania recznego prosze przelaczyc tryb")
        else:
            print ("jedzie do przodu")
            GPIO.output(11, GPIO.HIGH)
            GPIO.output(18, GPIO.HIGH)
    def silnik_tyl(self):
        if (self.sterowanie==1):
            print ("Wybrales sterowanie automatyczne, w celu sterowania recznego prosze przelaczyc tryb")
        else:
            print ("jedzie do tylu")
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(16, GPIO.HIGH)
            #drugi silnik
    def hamulec(self):
        if (self.sterowanie==1):
            print ("Wybrales sterowanie automatyczne, w celu sterowania recznego prosze przelaczyc tryb")
        else:
            print ("hamulec dziala")
            GPIO.output(11, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(16, GPIO.LOW)
            GPIO.output(18, GPIO.LOW)
            #zerowanie drugiego silnika
    def prawy(self):
        if (self.sterowanie==1):
            print ("Wybrales sterowanie automatyczne, w celu sterowania recznego prosze przelaczyc tryb")
        else:
            print("skreca w prawo")
            GPIO.output(11, GPIO.HIGH)

    def lewy(self):
        if (self.sterowanie==1):
            print ("Wybrales sterowanie automatyczne, w celu sterowania recznego prosze przelaczyc tryb")
        else:
            print("skreca w lewo")
            GPIO.output(18, GPIO.HIGH)
    def reczne_sterowanie(self):
        self.sterowanie=0
        print ("sterowanie reczne")
    def automatyczne_sterowanie(self):
        print ("sterowanie automatyczne")
        self.sterowanie=1
        
        
