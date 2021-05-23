from flask import Flask, request, Response
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Button, Servo, LineSensor
import board
from digitalio import DigitalInOut
import adafruit_character_lcd.character_lcd as characterlcd
from time import sleep

app = Flask(__name__)

# GPIO pins
button_pin = 26
servo_pin = 16
ir_pin = 27
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
servo = Servo(pin=servo_pin, initial_value=1, pin_factory=factory)

# Initialize ir
ir = LineSensor(ir_pin)

# Initialize lcd
lcd_columns = 16
lcd_rows = 2
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

# Global variables
normal_mode = True
count = 0

# Function to display lcd message (2nd line)
def set_lcd(message):
    lcd.clear()
    lcd.message = "Candy machine =)\n" + message

# Function to dispense one candy
def dispense():
    global normal_mode
    global count

    set_lcd("Dispensing candy")

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

    if normal_mode:
        set_lcd("")
    else:
        set_lcd("Count: " + str(count))

# Function to reset servo position
def reset():
    set_lcd("")

    value = servo.value
    shift = 0.1

    while value < 1:
        servo.value = value
        value += shift
        sleep(0.1)

# Function when ir is activated
def activate():
    global normal_mode
    global count

    if normal_mode:
        dispense()
    elif count > 0:
        count -= 1
        dispense()

# Function to switch mode
def switch_mode():
    global normal_mode
    global count

    normal_mode = not normal_mode

    if normal_mode:
        set_lcd("Mode: normal")
        sleep(1)
        set_lcd("")
    else:
        set_lcd("Mode: app")
        sleep(1)
        set_lcd("Count: " + str(count))

# Run
reset()
button.when_pressed = switch_mode
ir.when_line = activate

# Webhook
@app.route('/webhook', methods=['POST'])
def respond():
    global count

    if request.json['event_name'] == 'item:completed':
        count += 1
    elif request.json['event_name'] == 'item:uncompleted':
        count -= 1

    if not normal_mode:
        set_lcd("Count: " + str(count))

    return Response(status=200)