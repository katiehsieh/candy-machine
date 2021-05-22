from gpiozero import Button

button = Button(26)
counter = 0

try:
    while True:
        button.wait_for_press()
        counter += 1
        print(str(counter) + " Button Pressed")
        button.wait_for_release()

except KeyboardInterrupt:
    print("Done")