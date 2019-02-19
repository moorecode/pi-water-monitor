import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Reader():
    
    def rising_interrupt(self, channel):
        self.water_total += 1.0 / 5880.0 # in L (5880 pulses = 1L)

    def __init__(self, name, input_pin):
        self.name = name
        self.input_pin = input_pin
        self.water_total = 0
        self._last_read_time = time.time()
        GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(input_pin, GPIO.RISING, callback=self.rising_interrupt, bouncetime=5)  

    def read(self):
        value = self.water_total
        self.water_total = 0
        curr_time = time.time()
        duration = curr_time - self._last_read_time
        self._last_read_time = curr_time
        return (value, duration)
        
    def teardown(self):
        GPIO.cleanup(self.input_pin)




