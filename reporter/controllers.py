import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Controller():

    def __init__(self, name, output_pin):
        self.name = name
        self.output_pin = output_pin
        GPIO.setup(output_pin, GPIO.OUT)

    def set_state(self, on):
        try:
            if isinstance(on, str):
                on = True if on == "True" else False
            GPIO.output(self.output_pin, GPIO.HIGH if on else GPIO.LOW)
        except:
            print("##Error##")

    def teardown(self):
        GPIO.cleanup(self.output_pin)
