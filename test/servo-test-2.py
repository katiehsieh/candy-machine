# https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
# https://gpiozero.readthedocs.io/en/stable/api_output.html#servo

from gpiozero import Servo
from time import sleep

servo = Servo(16)
val = -1
shift = 0.1

try:
    while True:
        servo.value = val
        sleep(0.1)
        val = val + shift
        if val > 1:
            shift = shift * -1
            val = 1
        elif val < -1:
            shift = shift * -1
            val = -1

except KeyboardInterrupt:
    servo.detach()