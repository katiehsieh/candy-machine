# https://gpiozero.readthedocs.io/en/stable/api_input.html#lightsensor-ldr

from gpiozero import LightSensor

ldr = LightSensor(27)
counter = 0

print("IR Sensor Ready...")
print()

try:
    while True:
        ldr.wait_for_dark()
        counter += 1
        print(str(counter) + " Object Detected")
        ldr.wait_for_light()

except KeyboardInterrupt:
    print("Done")
