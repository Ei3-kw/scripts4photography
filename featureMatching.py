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
    # # grayscale
    # g1 = cv2.cvtColor(g1, cv2.COLOR_BGR2GRAY)
    # g2 = cv2.cvtColor(g2, cv2.COLOR_BGR2GRAY)

    # Compute keypoints & descriptors
    orb = cv2.ORB_create()
    k1, d1 = orb.detectAndCompute(g1, None)
    k2, d2 = orb.detectAndCompute(g2, None)

    # FLANN
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
    search_params = dict(checks=69) 

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(d1, d2, k=2)

    # Filter using Lowe's ratio test
    RATIO = 0.7
    good_matches = [m for m, n in matches if m.distance < RATIO * n.distance]

    return k1, k2, good_matches

if __name__ == '__main__':
    img_paths = select_images()

    if len(img_paths) != 2:
        print("Please select exactly two images.")
    else:
        img1 = cv2.imread(img_paths[0])
        img2 = cv2.imread(img_paths[1])
        img1 = cv2.resize(img1, (600, 800))
        img2 = cv2.resize(img2, (600, 800))

        mk1, mk2, good_matches = object_matching(img1, img2)

        matching_result = cv2.drawMatches(img1, mk1, img2, mk2, good_matches, None)

        cv2.imshow('Matching Result', matching_result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
