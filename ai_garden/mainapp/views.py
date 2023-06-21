import time
import datetime
import json
import random
import cv2

from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from collections import deque

import board
import adafruit_dht
import pwmio
import digitalio
from adafruit_motor import motor

from picamera2 import Picamera2

from .models import GardenPlan, PlantSpecification, Settings, WateringSchedule
from .utils import Table

# buffers
temp_0_buff, humidity_buff, soil_0_buff = deque(maxlen=1), deque(maxlen=1), deque(maxlen=1)

# init soil
soil_0 = digitalio.DigitalInOut(board.D4)
soil_0.direction = digitalio.Direction.INPUT
soil_0.pull = digitalio.Pull.DOWN

# init camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# init DHT22
dhtDevice = adafruit_dht.DHT22(board.D18)

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_a = pwmio.PWMOut(board.D23, frequency=1600)
pwm_b = pwmio.PWMOut(board.D24, frequency=1600)
pump_0 = motor.DCMotor(pwm_a, pwm_b)


def img_generator():
    while True:
        frame = picam2.capture_array()

        # compression
        ret, jpeg = cv2.imencode(".jpg", frame)

        time.sleep(0.04)  # 25 FPS
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )

def video_feed(request):
    return StreamingHttpResponse(
        img_generator(), content_type="multipart/x-mixed-replace;boundary=frame"
    )

def index(request):
    return render(request, "index.html")

def sensors(request):
    if "read" in request.GET and request.GET["read"] == "1":
        # get temp and humidity
        try:
            temp_0 = dhtDevice.temperature
            humidity_0 = dhtDevice.humidity
            
            temp_0_buff.append(temp_0)
            humidity_buff.append(humidity_0)
        except RuntimeError as e:
            temp_0 = temp_0_buff[-1]
            humidity_0 = humidity_buff[-1]
        except Exception as e:
            dhtDevice.exit()
            raise e

        # get soil
        soil_0_buff.append(int(not soil_0.value))

        return JsonResponse(
            {
                "Temperature 0": [temp_0, "°C", "[-40, 80]"],
                # "Temp 1": [round(random.random() * 3 + 28.5), "°C", "[-50, 150]"],
                # "Heat index": [round(random.random() * 3 + 31.5), "°C", "[-50, 150]"],
                "Humidity 0": [humidity_0, "%", "[0, 100]"],
                #"Pressure 0": [
                #    round(random.random() * 24 + 1004),
                #    "hPa",
                #    "[400, 1150]",
                #],
                "Soil moisture 0": [soil_0_buff[-1] * 100, "%", "[0, 100]"],
                #"Soil moisture 1": [round(random.random() * 12 + 74), "%", "[0, 100]"],
            }
        )
    else:
        return render(
            request,
            "sensors.html",
            {
                "refreshInterval": Settings.objects.values_list(
                    "refreshInterval", flat=True
                ).last()
            },
        )

def control(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        # run only if pots are dry
        if soil_0_buff[-1] == 0:
            pump_0.throttle = float(data['pump-0']) / 100.


    return render(request, "control.html")

def settings(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        # delete last settings
        if Settings.objects.count() > 0:
            Settings.objects.all().delete()

        # Create row with actual settings
        Settings.objects.create(
            selectedMode=data["mode"], refreshInterval=data["refreshInterval"]
        )

        # Delete selected items
        for row_id in data[f"del_{WateringSchedule.__name__}"]:
            WateringSchedule.objects.filter(pk=row_id).delete()

        # Add new items
        for row in data[f"new_{WateringSchedule.__name__}"]:
            WateringSchedule.objects.create(
                time=datetime.datetime.strptime(row[0], "%H:%M").time()
            )

        return HttpResponse(status=204)
    else:
        return render(
            request,
            "settings.html",
            context={
                "modes": ["Automatic", "Manual"],
                "selectedMode": Settings.objects.values_list(
                    "selectedMode", flat=True
                ).last(),
                "refreshInterval": Settings.objects.values_list(
                    "refreshInterval", flat=True
                ).last(),
                "wateringSchedule": Table(WateringSchedule),
            },
        )

def plants(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        # Delete selected items
        for row_id in data[f"del_{GardenPlan.__name__}"]:
            GardenPlan.objects.filter(pk=row_id).delete()
        for row_id in data[f"del_{PlantSpecification.__name__}"]:
            PlantSpecification.objects.filter(pk=row_id).delete()

        # Add new items
        for row in data[f"new_{GardenPlan.__name__}"]:
            GardenPlan.objects.create(
                p_type=row[0],
                p_variety=row[1],
                p_planting_date=datetime.datetime.strptime(row[2], "%Y-%m-%d").date(),
                p_location=row[3],
            )
        for row in data[f"new_{PlantSpecification.__name__}"]:
            PlantSpecification.objects.create(
                p_type=row[0],
                p_variety=row[1],
                p_num_of_seeds_in_1g=row[2],
                p_planting_date=row[3],
                p_planting_temp=row[4],
                p_planting_depth=row[5],
                p_germination_time=row[6],
                p_harvest_time=row[7],
                p_harvest_date=row[8],
                p_length_of_root=row[9],
                p_diameter=row[10],
                p_watering_time=datetime.datetime.strptime(row[11], "%H:%M").time(),
                p_class=row[12],
            )

        return HttpResponse(status=204)
    else:
        return render(
            request,
            "plants.html",
            context={
                "gardenPlan": Table(GardenPlan),
                "plantSpecification": Table(PlantSpecification),
            },
        )
