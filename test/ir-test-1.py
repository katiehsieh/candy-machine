# https://gpiozero.readthedocs.io/en/stable/api_input.html#linesensor-trct5000

from gpiozero import LineSensor
from signal import pause

sensor = LineSensor(27)
sensor.when_line = lambda: print('Line detected')
sensor.when_no_line = lambda: print('No line detected')
pause()