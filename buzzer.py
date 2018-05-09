import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(22, gpio.IN, pull_up_down = gpio.PUD_DOWN)

while True:            # this will carry on until you hit CTRL+C  
        if gpio.input(22): # if port 25 == 1  
            print ("Port 22 is 1/HIGH/True - LED ON" )
        else:  
            print ("Port 22 is 0/LOW/False - LED OFF" )
            
        time.sleep(1)
