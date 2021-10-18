import cv2
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.conf import settings

import random
import cv2
import os

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
        return render(request, 'sensors.html')

def control(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'control.html')

def settings(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'settings.html')

def plants(request):
    if request.method == 'POST':
        print(request.body)
    return render(request, 'plants.html')    

def img_generator(img):
    while True:
        ret, jpeg = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(img_generator(cv2.imread(IMG_FILE)),
					content_type='multipart/x-mixed-replace; boundary=frame')