import RPi.GPIO as GPIO
import cv2

GPIO.setmode(GPIO.BOARD)
blue = GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
white = GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if(GPIO.input(3) == 0):
        print("Button 1 pressed")
    if(GPIO.input(5) == 0):
        print("Button 2 pressed")


GPIO.cleanup()