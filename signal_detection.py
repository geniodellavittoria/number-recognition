
"""signal detection"""
import logging as log
import os
import cv2 as cv
import numpy as np
from skimage import measure
from imutils import resize, grab_contours
import prediction
from videocaptureasync import VideoCaptureAsync

VID = cv.VideoCapture('C:/Users/tbolz/Desktop/videos/video_40_ss_auto.h264')
CAP = VideoCaptureAsync('C:/Users/tbolz/Desktop/videos/video_40_ss_auto.h264')


def predict_number(sub_img):
    """calls prediction class to predict the number"""
    prediction.start(sub_img)


def detect_shape(cont, orig):
    """detects the square and crops it"""
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
                log.info("signal found with w: %s  h: %s", w, h)
                log.info("and ar:%s x:%s y:%s", ar, x, y)

                area = cv.contourArea(cont)
                hull_area = cv.contourArea(cv.convexHull(cont))
                solidity = area / float(hull_area)
                log.info(solidity)
                if solidity > 0.6:
                    cropped = orig[y:y+h, x:x+w]
                    predict_number(cropped)
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


def find_contours(frame):
    """finds the contours in a frame"""
    frame_resized = resize(frame.copy(), width=500)
    grayimg = cv.cvtColor(frame_resized, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(grayimg, (7, 7), 0)
    # high_thresh, thresh_im = cv.threshold(
    #     grayimg, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # lowThresh = 0.6*high_thresh

    cv.imshow("gray", grayimg)
    canny = cv.Canny(blurred, 100, 200)
    contours = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = grab_contours(contours)
    cv.imshow("closed", canny)
    for contour in contours:
        frame_resized = detect_shape(contour, frame_resized)
    return frame_resized


def img_dir():
    """directory with images is an input"""
    rootdir = 'images/'

    for files in os.walk(rootdir):
        for file in files:
            img(rootdir, file)


def img(rootdir, file):
    """image is an input"""
    log.debug("start to read img %s", file)
    image = cv.imread(rootdir + file)
    if image is None:
        log.error("img is null")
        quit()
    log.debug("img loaded succesfully")

    log.debug("start contour detection")
    image = find_contours(image)
    cv.imshow("frame", image)
    log.debug("finished contour detection")

    log.debug("wait until key is pressed")
    cv.waitKey(0)


def video():
    """use when video is input"""
    while VID.isOpened():
        try:
            # readimage
            frame = VID.read()[1]
            if frame is None:
                log.error("no frame")
                cleanup()
            image = find_contours(frame.copy())
            cv.imshow("el Image", image)

            cv.waitKey(0)
            # detect_portal(frame.copy())
            key = cv.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                cleanup()
                break
            if key == ord("p"):
                cv.waitKey(0)
        except KeyboardInterrupt:
            cleanup()


def cam():
    """use when camera is input"""
    CAP.start()
    while True:
        try:
            # readimage
            _, frame = CAP.read()
            log.error(frame)
            if frame is None:
                log.error("no frame")
                cleanup()
            image = find_contours(frame.copy())
            cv.imshow("el Image", image)
            key = cv.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                cleanup()
                break
            if key == ord("p"):
                cv.waitKey(0)
        except KeyboardInterrupt:
            cleanup()


def cleanup():
    """cleanup"""
    VID.release()
    cv.destroyAllWindows()


def main():
    """main"""
    log.basicConfig(level=log.DEBUG)
    log.info("program started")
    video()
    # cam()
    #img("", "images/image_4_weiss.png")
    # img_dir()


def detect_portal(frame):
    img = cv.resize(frame, (400, 500))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, gray = cv.threshold(gray, 127, 255, 0)
    gray2 = gray.copy()
    cv.imshow("gray", gray2)
    mask = np.zeros(gray.shape, np.uint8)
    contours, hier = cv.findContours(
        gray, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if 1000 < cv.contourArea(cnt) < 5000:
            log.info(cv.contourArea(cnt))
            cv.drawContours(img, [cnt], 0, (0, 255, 0), 2)
            cv.imshow("test", img)
            cv.waitKey(0)
            cv.drawContours(mask, [cnt], 0, 255, -1)


if __name__ == "__main__":
    main()
