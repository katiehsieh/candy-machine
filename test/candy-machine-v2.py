from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button, Servo, LightSensor
import board
from digitalio import DigitalInOut
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep

# GPIO pins
button_pin = 26
servo_pin = 16
ldr_pin = 27
lcd_rs = DigitalInOut(board.D25)
lcd_en = DigitalInOut(board.D24)
lcd_d7 = DigitalInOut(board.D22)
lcd_d6 = DigitalInOut(board.D18)
lcd_d5 = DigitalInOut(board.D17)
lcd_d4 = DigitalInOut(board.D23)

# Initialize button
button = Button(button_pin)

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

# Variables
normalMode = True

# Function to display lcd message
def set_lcd(message):
    lcd.clear()
    lcd.message = message

# Function to dispense one candy
def dispense():
    lcd.clear()
    set_lcd("Candy machine =)\nDispensing candy")

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

    set_lcd("Candy machine =)")

# Function to reset servo position
def reset():
    lcd.clear()
    value = servo.value
    shift = 0.1
    while value < 1:
        servo.value = value
        value += shift
        sleep(0.1)

# Function when ldr is activated
def ldr_activate():
    global normalMode
    if normalMode:
        dispense()

# Function to switch mode
def switch_mode():
    global normalMode
    normalMode = not normalMode
    if normalMode:
        set_lcd("Candy machine =)\nMode: normal")
        sleep(1)
        set_lcd("Candy machine =)")
    else:
        set_lcd("Candy machine =)\nMode: app")
        sleep(1)
        set_lcd("Candy machine =)")

set_lcd("Candy machine =)")
button.when_pressed = switch_mode
ldr.when_dark = ldr_activate