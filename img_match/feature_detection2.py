"""feature detection."""

#値が小さいほど類似度が高い

import cv2
import os
import math
import numpy as np

TARGET_FILE = '2002.png'
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/kanzi/'
IMG_SIZE = (400, 400)

target_img_path = IMG_DIR + TARGET_FILE

# グレースケールに変換
target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
target_img = cv2.resize(target_img, IMG_SIZE)

# ２値化＋ノイズ除去
retval, bw = cv2.threshold(target_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
bw2 = cv2.adaptiveThreshold(target_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 10)

# 表示
cv2.imshow('output', bw2)
cv2.waitKey(0)

# 終了処理
cv2.destroyAllWindows()
