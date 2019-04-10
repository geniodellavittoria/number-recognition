import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import logging as log

log.basicConfig(level=log.DEBUG)
log.info("program started")


def start(subImg):

    # Load the kNN Model
    with np.load('knn_data.npz') as data:
        print(data.files)
        train = data['train']
        train_labels = data['train_labels']

    cv.imshow("testImg", subImg)
    knn = cv.ml.KNearest_create()
    knn.train(train, cv.ml.ROW_SAMPLE, train_labels)
    img_gray = cv.cvtColor(subImg, cv.COLOR_BGR2GRAY)
    (thresh, img) = cv.threshold(img_gray,
                                 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    sub_bw = cv.threshold(img, thresh, 255, cv.THRESH_BINARY_INV)[1]

    img_resized = cv.resize(img_gray, (20, 20))

    cv.imshow("gray", img_gray)
    x = np.array(img_resized)
    test_img = x.reshape(-1, 400).astype(np.float32)
    ret, result, neighbours, dist = knn.findNearest(test_img, k=1)
    # Print the predicted number
    print(result)
