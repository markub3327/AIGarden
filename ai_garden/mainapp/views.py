import datetime
import json
import random
import lgpio

from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render

from .models import GardenPlan, PlantSpecification, Settings, WateringSchedule
from .utils import Table

# init GPIO
h = lgpio.gpiochip_open(0)

def index(request):
    return render(request, "index.html")

def sensors(request):
    if "read" in request.GET and request.GET["read"] == "1":
        return JsonResponse(
            {
                "Temp 0": [round(random.random() * 30), "°C", "[-50, 150]"],
                "Temp 1": [round(random.random() * 30), "°C", "[-50, 150]"],
                "Heat index": [round(random.random() * 35), "°C", "[-50, 150]"],
                "Humidity 0": [round(random.random() * 35), "%", "[0, 100]"],
                "Pressure 0": [
                    round(random.random() * 1016),
                    "hPa",
                    "[400, 1150]",
                ],
                "Soil moisture 0": [round(random.random() * 80), "%", "[0, 100]"],
                "Soil moisture 1": [round(random.random() * 80), "%", "[0, 100]"],
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
        print(data)

        # set the pump
        lgpio.tx_pwm(h, 18, 10000, int(data['pump-0']))

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