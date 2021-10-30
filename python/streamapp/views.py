from typing import Set
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.conf import settings
from .models import Settings, WateringSchedule, Modes
from .utils import config
from .utils.imgutils import imresize
from scipy import ndimage
from .modules.solov2 import SOLOV2
from .utils.config import cfg

import numpy as np
import random
import cv2
import os
import json
import datetime
import torch

IMG_FILE = os.path.join(settings.BASE_DIR, 'video.jpg')

# Load model
model = SOLOV2(cfg, pretrained=os.path.join(settings.BASE_DIR, 'models/solov2_448_r18_epoch_36.pth'), mode='test')

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
            #print(t)
            #WateringSchedule.objects.filter(time=t).delete()
        
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
        while True:
            img_cam = cv2.imread(IMG_FILE)

            # Preprocess the input image
            img_cam = cv2.copyMakeBorder(
                img_cam, 280, 280, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0]
            )  # zero-padding
            img = cv2.cvtColor(img_cam, cv2.COLOR_BGR2RGB)
            img = img.transpose(2, 0, 1)
            img = img.astype(np.float32)

            # global standardization of pixels
            img[0, :, :] = (img[0, :, :] - config.MEANS[0]) / config.STD[0]
            img[1, :, :] = (img[1, :, :] - config.MEANS[1]) / config.STD[1]
            img[2, :, :] = (img[2, :, :] - config.MEANS[2]) / config.STD[2]

            img = torch.from_numpy(img).unsqueeze(0)

            with torch.no_grad():
                seg_result = model.simple_test(
                    img=img,
                    img_meta=[{
                        "ori_shape": img_cam.shape,
                        "img_shape": img_cam.shape,
                        "scale_factor": 1
                    }]
                )
            img_cam = show_result_ins(img_cam, seg_result)
            img_cam = img_cam[280:-280, :, :]

            ret, jpeg = cv2.imencode('.jpg', img_cam)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
 
def video_feed(request):
    return StreamingHttpResponse(img_generator(), content_type="multipart/x-mixed-replace;boundary=frame")

def show_result_ins(img,
                        result,
                        score_thr=0.3,
                        sort_by_density=False):
        h, w, _ = img.shape

        cur_result = result[0]
        seg_label = cur_result[0]
        seg_label = seg_label.cpu().numpy().astype(np.uint8)
        cate_label = cur_result[1]
        cate_label = cate_label.cpu().numpy()
        score = cur_result[2].cpu().numpy()

        vis_inds = score > score_thr
        seg_label = seg_label[vis_inds]
        num_mask = seg_label.shape[0]
        cate_label = cate_label[vis_inds]
        cate_score = score[vis_inds]

        if sort_by_density:
            mask_density = []
            for idx in range(num_mask):
                cur_mask = seg_label[idx, :, :]
                cur_mask = imresize(cur_mask, (w, h))
                cur_mask = (cur_mask > 0.5).astype(np.int32)
                mask_density.append(cur_mask.sum())
            orders = np.argsort(mask_density)
            seg_label = seg_label[orders]
            cate_label = cate_label[orders]
            cate_score = cate_score[orders]

        np.random.seed(42)
        color_masks = [
            np.random.randint(0, 256, (1, 3), dtype=np.uint8)
            for _ in range(num_mask)
        ]
        #img_show = None
        for idx in range(num_mask):
            idx = -(idx+1)
            cur_mask = seg_label[idx, :, :]
            cur_mask = imresize(cur_mask, (w, h))
            cur_mask = (cur_mask > 0.5).astype(np.uint8)
            if cur_mask.sum() == 0:
                continue
            color_mask = color_masks[idx]
            cur_mask_bool = cur_mask.astype(np.bool)
            img[cur_mask_bool] = img[cur_mask_bool] * 0.5 + color_mask * 0.5

            #当前实例的类别
            cur_cate = cate_label[idx]
            realclass = config.COCO_LABEL[cur_cate]
            cur_score = cate_score[idx]

            name_idx = config.COCO_LABEL_MAP[realclass]
            label_text = config.COCO_CLASSES[name_idx-1]
            label_text += '|{:.02f}'.format(cur_score)
            center_y, center_x = ndimage.measurements.center_of_mass(cur_mask)
            vis_pos = (max(int(center_x) - 10, 0), int(center_y))
            cv2.putText(img, label_text, vis_pos,
                            cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 255))  # green
 
        return img
