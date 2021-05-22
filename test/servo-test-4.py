# https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
# https://gpiozero.readthedocs.io/en/stable/api_output.html#servo
# https://gpiozero.readthedocs.io/en/stable/api_pins.html#module-gpiozero.pins.pigpio
# sudo pigpiod

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
from time import sleep

factory = PiGPIOFactory()
servo = Servo(16, min_pulse_width=5/10000, max_pulse_width=25/10000, pin_factory=factory)
val = servo.value
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
    servo.max()