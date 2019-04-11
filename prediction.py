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

    sub_bw = cv.threshold(img_gray, 180, 255, cv.THRESH_BINARY_INV)[1]
    # imgBackground = blackWhiteDetection(img_gray)
    # log.info(imgBackground)
    # if (imgBackground == "white"):
    #     sub_bw = cv.threshold(img_gray, 180, 255, cv.THRESH_BINARY_INV)[1]
    # else:
    #     sub_bw=
    img_resized = cv.resize(sub_bw, (20, 20))

    cv.imshow("gray", sub_bw)
    x = np.array(img_resized)
    test_img = x.reshape(-1, 400).astype(np.float32)
    ret, result, neighbours, dist = knn.findNearest(test_img, k=1)
    # Print the predicted number
    print(result)


# def blackWhiteDetection(img):
#     a = [50, 51, 52, 53, 54, 55]
#     pixel = 0
#     for i in a:
#         pixel = img[10, i+10] + pixel

#     if pixel.mean() > 200:
#         print("white")
#         return "white"
#     else:
#         print("black")
#         return "black"
