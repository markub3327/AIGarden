import RPi.GPIO as GPIO
from time import sleep
import os

# Watering
def watering(motor):
    for force in range(1,101,1):
        motor.ChangeDutyCycle(force)
        sleep(0.5)
        print(f"Watering ... {force} %")
    sleep(5)
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
motor1_pwm = GPIO.PWM(motor1_pin, 1000)     # 1kHz
motor1_pwm.start(0)
motor2_pwm = GPIO.PWM(motor2_pin, 1000)     # 1kHz
motor2_pwm.start(0)

# Main loop
while True:
    print("AIGarden 🚰🥕🍅")
    print("Bc. Martin Kubovčík")
    print("https://github.com/markub3327/AIGarden")
    print()
    print("        1  Watering")
    print("        2  Scan")
    print("        3  Scan")
    print("        q  Quit")
    print()
    cmd = input(">> ")

    if cmd == "1":
        watering(motor1_pwm)
        watering(motor2_pwm)
    elif cmd == "2":
        print("Scanning ...")
    elif cmd == "3":
        end = False
        while end == False:
            print("Settings")
            print("        q  Quit")
            print()
            cmd = input(">> ")

            if cmd == 'q':
                break
            else:
                print("Bad command was eneterd.")
    else:
        print("Bad command was eneterd.")
    
    clear()     # clear console
