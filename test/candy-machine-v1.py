from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo, LightSensor
import board
from digitalio import DigitalInOut
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep

# GPIO pins
servo_pin = 16
ldr_pin = 27
lcd_rs = DigitalInOut(board.D25)
lcd_en = DigitalInOut(board.D24)
lcd_d7 = DigitalInOut(board.D22)
lcd_d6 = DigitalInOut(board.D18)
lcd_d5 = DigitalInOut(board.D17)
lcd_d4 = DigitalInOut(board.D23)

# Initialize servo
factory = PiGPIOFactory()
servo = Servo(pin=servo_pin, initial_value=1, min_pulse_width=5/10000, max_pulse_width=25/10000, pin_factory=factory)

# Initialize ldr
ldr = LightSensor(ldr_pin)

# Initialize lcd
lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)
lcd.message = "Candy machine =)"

# Function to dispense one candy
def dispense():
    lcd.message = "Candy machine =)\nDispensing candy"

    value = servo.value
    shift = 0.1

    while value > -1:
        servo.value = value
        value -= shift
        sleep(0.1)

    value = -1

    while value < 1:
        servo.value = value
        value += shift
        sleep(0.1)

    lcd.clear()
    lcd.message = "Candy machine =)"

# Function to reset servo position
def reset():
    lcd.clear()
    value = servo.value
    shift = 0.1
    while value < 1:
        servo.value = value
        value += shift
        sleep(0.1)

# Main loop
try:
    while True:
        ldr.wait_for_dark()
        dispense()
        ldr.wait_for_light()

except KeyboardInterrupt:
    print("done")
    reset()