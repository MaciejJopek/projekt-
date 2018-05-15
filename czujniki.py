import RPi.GPIO as GPIO
class Sensory(object):       
    def silnik_przod(self):
        print ("jedzie do przodu")
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(18, GPIO.HIGH)
    def silnik_tyl(self):
        print ("jedzie do tylu")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.HIGH)
            
    def hamulec(self):
        print ("hamulec dziala")
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
            
    def prawy(self):
        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.HIGH)

    def lewy(self):
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)

        
        
