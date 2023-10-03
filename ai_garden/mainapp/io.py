import threading
import time
from collections import deque

import board
import adafruit_dht
import pwmio
import digitalio
from adafruit_motor import motor

# buffers
temp_0_buff, humidity_buff, soil_0_buff = deque([0], maxlen=1), deque([0], maxlen=1), deque([0], maxlen=1)

# init soil
soil_0 = digitalio.DigitalInOut(board.D4)
soil_0.direction = digitalio.Direction.INPUT
soil_0.pull = digitalio.Pull.DOWN

# init DHT22
dhtDevice = adafruit_dht.DHT22(board.D18)

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_a = pwmio.PWMOut(board.D23, frequency=1600)
pwm_b = pwmio.PWMOut(board.D24, frequency=1600)
pump_0 = motor.DCMotor(pwm_a, pwm_b)

def worker():
    while True:
        # get temp and humidity
        try:
            temp_0_buff.append(dhtDevice.temperature)
            humidity_buff.append(dhtDevice.humidity)
        except RuntimeError as e:
            time.sleep(2.0)
        except Exception as e:
            dhtDevice.exit()
            raise e

        # get soil
        soil_0_buff.append(int(not soil_0.value))
        
        # stop pumps if pots are saturated
        if soil_0_buff[-1] > 0:
            pump_0.throttle = 0.0

# creating thread
control_thread = threading.Thread(target=worker, daemon=True)

# starting thread
control_thread.start()
