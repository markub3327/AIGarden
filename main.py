import RPi.GPIO as GPIO
from time import sleep
import os

# Watering
def watering(motor, duration):
    # start pump
    for duty in range(1, 101, 1):
        motor.ChangeDutyCycle(duty)
        sleep(0.05)

    # waiting ...
    for t in range(1, 101, 1):
        sleep(duration / 100.0)
        print(f"Task Completed ... {t}%", end='\r')

    # stop pump
    motor.ChangeDutyCycle(0)

# Init console
clear = lambda: os.system('clear')

# Init GPIO
GPIO.setmode(GPIO.BOARD)

# Pumps
motor1_pin = 32
motor2_pin = 33
GPIO.setup(motor1_pin, GPIO.OUT)
GPIO.setup(motor2_pin, GPIO.OUT)
motor1_pwm = GPIO.PWM(motor1_pin, 10000)     # 10 kHz
motor1_pwm.start(0)
motor2_pwm = GPIO.PWM(motor2_pin, 10000)     # 10 kHz
motor2_pwm.start(0)

# Main loop
while True:
    print("AIGarden 🚰🥕🍅")
    print("Bc. Martin Kubovčík")
    print("https://github.com/markub3327/AIGarden")
    print()
    print("        1  Watering 🚰")
    print("        2  Scan 👀")
    print("        3  Settings ⚙️")
    print("        q  Quit 🚪")
    print()
    cmd = input(">> ")

    if cmd == "1":
        clear()     # clear console
        watering(motor1_pwm, 60)
        #watering(motor2_pwm)
    elif cmd == "2":
        clear()     # clear console
        print("Scanning ...")
    elif cmd == "3":
        clear()     # clear console
        end = False
        while end == False:
            print("Settings ⚙️")
            print("        q  Quit 🚪")
            print()
            cmd = input(">> ")

            if cmd == 'q':
                clear()     # clear console
                break
            else:
                print("Bad command was eneterd.")
    elif cmd == 'q':
        print("Terminated by user 👋👋👋")
        exit()
    else:
        print("Bad command was eneterd.")