# https://www.electronicshub.org/interfacing-ir-sensor-with-raspberry-pi/

import RPi.GPIO as GPIO
import time

sensor = 13
counter = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)

print("IR Sensor Ready...")
print()

try:
    while True:
        if GPIO.input(sensor):
            counter += 1
            print(str(counter) + " Object Detected")
            while GPIO.input(sensor):
                time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()