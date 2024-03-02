import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_images():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilenames(
        title='Select images',
        filetypes=[('Image files', '.jpg .png')])

def object_matching(g1, g2):
    g1 = cv2.cvtColor(g1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(g2, cv2.COLOR_BGR2GRAY)

    # Compute keypoints & descriptors
    orb = cv2.ORB_create()
    k1, d1 = orb.detectAndCompute(g1, None)
    k2, d2 = orb.detectAndCompute(g2, None)

    # FLANN
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=50)  # You can adjust the checks parameter

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(d1, d2, k=2)

    # Filter using Lowe's ratio test
    RATIO = 0.7
    good_matches = [m for m, n in matches if m.distance < RATIO * n.distance]

    return k1, k2, good_matches

def yolo_object_detection(image_path):
    net = cv2.dnn.readNet("yolov7.weights", "yolov7.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f]

    layer_names = net.getUnconnectedOutLayersNames()

    image = cv2.imread(image_path)
    height, width, _ = image.shape

    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    detected_objects = []
    for i in indices:
        i = i[0]
        box = boxes[i]
        detected_objects.append((box[0], box[1], box[0] + box[2], box[1] + box[3]))

    return detected_objects

def match_objects_using_bounding_boxes(objects1, objects2):
    matched_boxes1 = []
    matched_boxes2 = []

    for box1 in objects1:
        for box2 in objects2:
            if overlap(box1, box2) > 0.5:  # Tweak the overlap threshold as needed
                matched_boxes1.append(box1)
                matched_boxes2.append(box2)

    return np.array(matched_boxes1), np.array(matched_boxes2)

def overlap(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2

    overlap_x = max(0, min(x2, x4) - max(x1, x3))
    overlap_y = max(0, min(y2, y4) - max(y1, y3))

    area_overlap = overlap_x * overlap_y
    area_box1 = (x2 - x1) * (y2 - y1)
    area_box2 = (x4 - x3) * (y4 - y3)

    intersection_over_union = area_overlap / float(area_box1 + area_box2 - area_overlap)
    return intersection_over_union

if __name__ == '__main__':
    img_paths = select_images()

    if len(img_paths) != 2:
        print("Please select exactly two images.")
    else:
        img1 = cv2.imread(img_paths[0])
        img2 = cv2.imread(img_paths[1])
        img1 = cv2.resize(img1, (600, 800))
        img2 = cv2.resize(img2, (600, 800))

        # Object Matching based on Key Features
        mk1, mk2, good_matches = object_matching(img1, img2)

        # YOLO Object Detection
        detected_objects1 = yolo_object_detection(img_paths[0])
        detected_objects2 = yolo
