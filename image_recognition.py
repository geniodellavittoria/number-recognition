import cv2 as cv
import datetime
import argparse
import time
import numpy as np
import logging as log
from time import sleep
import imutils
from imutils import contours
from imutils.video import VideoStream

croppedImages = []

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())


def save(img):
    current = str(time.time())
    name = 'Frames/frame_' + current + '.png'
    cv.imwrite(name, img)
    return name


def crop(x, y, w, h, img):
    # crop the image using array slices -- it's a NumPy array
    cropped = img[y:y+h, x:x+w]
    croppedImages.append(cropped)


def detectShape(cont, orig):
    # compute the bounding box of the contour and use the
    # bounding box to compute the aspect ratio
    peri = cv.arcLength(cont, True)
    approx = cv.approxPolyDP(cont, 0.04 * peri, True)
    (x, y, w, h) = cv.boundingRect(approx)
    ar = w / float(h)
    print(ar)
    if len(approx) == 4:
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square" if ar >= 0.95 and ar <= 1.15 else "rectangle"
        if shape == "square":
            subimg = orig[y: y + h, x: x + w, :]
            cv.imshow("subImg", subimg)
            cv.imwrite("subimg.png", subimg)
            return subimg
        log.debug(ar)
        return None


def findContours(edged, orig):
    cv.threshold(edged, 60, 255, cv.THRESH_BINARY)[1]
    edged = cv.GaussianBlur(edged, (5, 5), 0)
    cnts = cv.findContours(edged, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        # detect the name of the shape
        detectShape(c, orig)
        cv.drawContours(orig, [c], -1, (0, 255, 0), 2)


def processImage(orig):
    # prepare(src,img)
    # findContours(img,orig)
    for img in croppedImages:
        print("cropped")
        # predict(img)
      # predict(img)


def img():
    log.debug("start to read img")
    image = cv.imread("image_test_2.png")
    if image is None:
        log.error("img is null")
    log.debug("img loaded succesfully")

    log.debug("start canny")
    log.debug(image.shape)
    resized = imutils.resize(image, width=300)
    edged = imutils.auto_canny(resized)

    log.debug("show canny")
    cv.imshow("sss", edged)

    log.debug("start contour detection")
    findContours(edged, resized)
    log.debug("finished contour detection")

    log.debug("wait until key is pressed")
    cv.waitKey(0)


def pycam():
    # loop over the frames from the video stream
    # initialize the video stream and allow the cammera sensor to warmup

    cap = cv.VideoCapture(-1)
    time.sleep(10.0)
    while True:
        try:
            # readimage
            frame = cap.read()[1]
            frame = imutils.resize(frame, width=300)
            cv.imshow("Window", frame)
            key = cv.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
                # do a bit of cleanup
                cap.release()
                cv.destroyAllWindows()
            elif key == ord("c"):
                processImage(frame)
                pass
        except KeyboardInterrupt:
            # do a bit of cleanup
            cap.release()
            cv.destroyAllWindows()


def main():
    log.basicConfig(level=log.DEBUG)
    log.info("program started")
    # pycam()
    img()


if __name__ == "__main__":
    main()
