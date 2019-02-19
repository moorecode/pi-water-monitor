import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  

num = 0
  
# GPIO 23 & 17 set up as inputs, pulled up to avoid false detection.  
# Both ports are wired to connect to GND on button press.  
# So we'll be setting up falling edge detection for both  
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
  
# now we'll define two threaded callback functions  
# these will run in another thread when our events are detected  
def my_callback(channel):  
    print("falling edge detected on 17")
  
def my_callback2(channel):  
    print(str(channel) + " falling edge detected on 23")
  
print("Make sure you have a button connected so that when pressed")
print("it will connect GPIO port 23 (pin 16) to GND (pin 6)\n")
print("You will also need a second button connected so that when pressed")
print("it will connect GPIO port 24 (pin 18) to 3V3 (pin 1)\n")
print("You will also need a third button connected so that when pressed")
print("it will connect GPIO port 17 (pin 11) to GND (pin 14)")
  
  
# when a falling edge is detected on port 23, regardless of whatever   
# else is happening in the program, the function my_callback2 will be run  
# 'bouncetime=300' includes the bounce control written into interrupts2a.py  
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=1) 
  
try:  
    while True:
        pass
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  