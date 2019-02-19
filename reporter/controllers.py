import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Controller():

    def __init__(self, name, output_pin):
        self.name = name
        self.output_pin = output_pin
        GPIO.setup(output_pin, GPIO.OUT)

    def set_state(self, on):
        print("set pin state " + str(self.output_pin) + ("on" if on else "off"))
        GPIO.output(self.output_pin, GPIO.HIGH if on else GPIO.LOW)

    def teardown(self):
        GPIO.cleanup()