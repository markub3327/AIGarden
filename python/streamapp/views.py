import datetime
import json
import os
import random

import cv2
import numpy as np
import torch
from django.conf import settings
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from scipy import ndimage

from .models import GardenPlan, PlantSpecification, Settings, WateringSchedule
from .modules.solov2 import SOLOV2
from .utils import Table, cfg, config
from .utils.imgutils import imresize

IMG_FILE = os.path.join(settings.BASE_DIR, "video.jpg")

# Load model
model = SOLOV2(
    cfg,
    pretrained=os.path.join(settings.BASE_DIR, "models/solov2_448_r18_epoch_36.pth"),
    mode="test",
)
# model = model.cuda()


def index(request):
    return render(request, "index.html")


def sensors(request):
    if "read" in request.GET and request.GET["read"] == "1":
        return JsonResponse(
            {
                "Temp 0": [round(random.random() * 200 - 50), "°C", "[-50, 150]"],
                "Temp 1": [round(random.random() * 200 - 50), "°C", "[-50, 150]"],
                "Heat index": [round(random.random() * 200 - 50), "°C", "[-50, 150]"],
                "Humidity 0": [round(random.random() * 100), "%", "[0, 100]"],
                "Pressure 0": [round(random.random() * 750 + 400), "hPa", "[400, 1150]"],
                "Soil moisture 0": [round(random.random() * 100), "%", "[0, 100]"],
                "Soil moisture 1": [round(random.random() * 100), "%", "[0, 100]"],
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
        print(request.body)
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
            print(row)
            GardenPlan.objects.create(
                p_type=row[0],
                p_variety=row[1],
                p_planting_date=datetime.datetime.strptime(row[2], "%d.%m.%Y").date(),
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
                p_watering_time=datetime.datetime.strptime(row[10], "%H:%M").time(),
                p_class=row[11],
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

        # Normalization of image
        # 1. step 
        img = img / 255.0
        # 2. step
        img[0, :, :] = (img[0, :, :] - config.MEAN[0]) / config.STD[0]
        img[1, :, :] = (img[1, :, :] - config.MEAN[1]) / config.STD[1]
        img[2, :, :] = (img[2, :, :] - config.MEAN[2]) / config.STD[2]

        # img = torch.from_numpy(img).cuda().unsqueeze(0)
        img = torch.from_numpy(img).unsqueeze(0)

        with torch.no_grad():
            seg_result = model.simple_test(
                img=img,
                img_meta=[
                    {
                        "ori_shape": img_cam.shape,
                        "img_shape": img_cam.shape,
                        "scale_factor": 1,
                    }
                ],
            )
        if not None in seg_result:
            img_cam = show_result_ins(img_cam, seg_result)
        img_cam = img_cam[280:-280, :, :]

        ret, jpeg = cv2.imencode(".jpg", img_cam)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
        )


def video_feed(request):
    return StreamingHttpResponse(
        img_generator(), content_type="multipart/x-mixed-replace;boundary=frame"
    )


def show_result_ins(img, result, score_thr=0.3, sort_by_density=False):
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
        np.random.randint(0, 256, (1, 3), dtype=np.uint8) for _ in range(num_mask)
    ]
    # img_show = None
    for idx in range(num_mask):
        idx = -(idx + 1)
        cur_mask = seg_label[idx, :, :]
        cur_mask = imresize(cur_mask, (w, h))
        cur_mask = (cur_mask > 0.5).astype(np.uint8)
        if cur_mask.sum() == 0:
            continue
        color_mask = color_masks[idx]
        cur_mask_bool = cur_mask.astype(np.bool)
        img[cur_mask_bool] = img[cur_mask_bool] * 0.5 + color_mask * 0.5

        # 当前实例的类别
        cur_cate = cate_label[idx]
        realclass = config.COCO_LABEL[cur_cate]
        cur_score = cate_score[idx]

        name_idx = config.COCO_LABEL_MAP[realclass]
        label_text = config.COCO_CLASSES[name_idx - 1]
        label_text += "|{:.02f}".format(cur_score)
        center_y, center_x = ndimage.measurements.center_of_mass(cur_mask)
        vis_pos = (max(int(center_x) - 10, 0), int(center_y))
        cv2.putText(
            img, label_text, vis_pos, cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 255)
        )  # green

    return img
