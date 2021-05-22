# https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/

import RPi.GPIO as GPIO
import time

servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 16 for PWM with 50Hz
p.start(2.5) # Initialization

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(servoPIN, True)
	p.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(servoPIN, False)
	p.ChangeDutyCycle(0)

SetAngle(90)
time.sleep(5)
SetAngle(0)
time.sleep(5)
SetAngle(180)

p.stop()
GPIO.cleanup()