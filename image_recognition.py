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
import prediction
import os

cap = cv.VideoCapture('C:/Users/tbolz/Desktop/videos/video_20_ss_auto.h264')


def predictNumber(subImg):
    prediction.start(subImg)


def detectShape(cont, orig):
    # compute the bounding box of the contour and use the
    # bounding box to compute the aspect ratio
    peri = cv.arcLength(cont, True)
    approx = cv.approxPolyDP(cont, 0.02*peri, True)
    (x, y, w, h) = cv.boundingRect(approx)
    ar = w / float(h)
    if len(approx) == 4:
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "square" if ar >= 0.95 and ar <= 1.1 else "rectangle"
        if shape == "square":
            if w > 15 and h > 15:
                log.info("signal found with w: " + str(w) + "  h: " + str(h))
                log.info("and ar:"+str(ar)+" x:"+str(x)+" y:"+str(y))

                area = cv.contourArea(cont)
                hullArea = cv.contourArea(cv.convexHull(cont))
                solidity = area / float(hullArea)
                log.info(solidity)
                if solidity > 0.6:
                    cropped = orig[y:y+h, x:x+w]
                    predictNumber(cropped)
                    cv.drawContours(orig, [cont], -1, (0, 255, 0), 2)
                    cv.imshow("with green lines", orig)
                    cv.waitKey(0)
                else:
                    log.info("not square alike")
                    cv.drawContours(orig, [cont], -1, (255, 0, 0), 2)
            else:
                log.info("too small square found")
                cv.drawContours(orig, [cont], -1, (0, 0, 255), 2)
    else:
        cv.drawContours(orig, [cont], -1, (0, 0, 255), 2)
    return orig


def findContours(frame):
    frame_resized = imutils.resize(frame.copy(), width=500)
    grayimg = cv.cvtColor(frame_resized, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grayimg, (7, 7), 0)
    # high_thresh, thresh_im = cv.threshold(
    #     grayimg, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # lowThresh = 0.6*high_thresh

    cv.imshow("gray", grayimg)
    canny = cv.Canny(blurred, 100, 200)
    cnts = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv.imshow("closed", canny)
    for c in cnts:
        # detect the name of the shape
        frame_resized = detectShape(c, frame_resized)
    return frame_resized


def imgDir():
    rootdir = 'images/'

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            img(rootdir, file)


def img(rootdir, file):
    log.debug('start to read img ' + file)
    image = cv.imread(rootdir + file)
    if image is None:
        log.error("img is null")
        quit()
    log.debug("img loaded succesfully")

    log.debug("start contour detection")
    image = findContours(image)
    cv.imshow("frame", image)
    log.debug("finished contour detection")

    log.debug("wait until key is pressed")
    cv.waitKey(0)


def cam():
    # loop over the frames from the video stream
    # initialize the video stream and allow the cammera sensor to warmup

    while cap.isOpened():
        try:
            # readimage
            frame = cap.read()[1]
            if frame is None:
                log.error("no frame")
                cleanup()
            image = findContours(frame.copy())
            cv.imshow("el Image", image)
            key = cv.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
                # do a bit of cleanup
                cap.release()
                cv.destroyAllWindows()
            if key == ord("p"):
                cv.waitKey(0)
        except KeyboardInterrupt:
            cleanup()


def cleanup():
    cap.release()
    cv.destroyAllWindows()


def main():
    log.basicConfig(level=log.DEBUG)
    log.info("program started")
    cam()
    #img("", "images/image_4_weiss.png")
    # imgDir()


if __name__ == "__main__":
    main()
