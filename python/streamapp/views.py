from typing import Set
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.conf import settings
from .models import Settings, WateringSchedule, Modes

import random
import cv2
import os
import json
import datetime

IMG_FILE = os.path.join(settings.BASE_DIR, 'video.jpg')


def index(request):
    return render(request, 'index.html')

def sensors(request):
    if 'read' in request.GET and request.GET['read'] == '1':
        return JsonResponse({
            "Temp 0": random.random(),
            "Temp 1": random.random(),
            "Heat index": random.random(),
            "Humidity 0": random.random(),
            "Pressure 0": random.random(),
            "Soil 0": random.random(),
            "Soil 1": random.random(),
        })
    else:
        return render(request, 'sensors.html', {'refresh_interval': Settings.objects.values_list('refreshInterval', flat=True).last()})

def control(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'control.html')

def settings(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # delete last settings
        if Settings.objects.count() > 0:
            Settings.objects.all().delete()

        # Create row with actual settings
        Settings.objects.create(selectedMode=data['mode'], refreshInterval=data['refresh_interval'])

        # Delete selected times
        for t in data['del_watering_schedule']:
            _t = datetime.datetime.strptime(t, '%H:%M')
            WateringSchedule.objects.filter(time__hour=_t.hour, time__minute=_t.minute).delete()
        
        # Add new times
        for t in data['new_watering_schedule']:
            WateringSchedule.objects.create(time=datetime.datetime.strptime(t, '%H:%M').time())

        return HttpResponse(status=204)
    else:
        return render(request, 'settings.html', {
            'modes': Modes.objects.values_list('mode', flat=True),
            'selectedMode': Settings.objects.values_list('selectedMode', flat=True).last(),
            'refresh_interval': Settings.objects.values_list('refreshInterval', flat=True).last(),
            'watering_schedule': [t.strftime("%H:%M") for t in WateringSchedule.objects.all().order_by('time__hour').values_list('time', flat=True)]
        })

def plants(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'plants.html')    

def img_generator():
    img_cam = cv2.imread(IMG_FILE)
    # Preprocess the input image
    img_cam = cv2.copyMakeBorder(
        img_cam, 280, 280, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0]
    )  # zero-padding

    while True:
        ret, jpeg = cv2.imencode('.jpg', img_cam)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(img_generator(), content_type="multipart/x-mixed-replace;boundary=frame")
