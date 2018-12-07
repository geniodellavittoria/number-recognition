
# 1. read image
# 2. convert to gray scale
# 3. convert to uint8 range
# 4. threshold via otsu method
# 5. resize image
# 6. invert image to balck background
# 7. Feed into trained neural network
# 8. print answer

#from skimage.io import imread
from skimage import img_as_ubyte  # convert float to uint8
import cv2 as cv
import datetime
import argparse
import imutils
import time
import numpy as np

from time import sleep
from imutils.video import VideoStream
##from keras.models import load_model

# import CNN model weight
##model = load_model(r'.\\mnist_trained_model.h5')
croppedImages = []

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--picamera", type=int, default=-1,
#                 help="whether or not the Raspberry Pi camera should be used")
# args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
#vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
cap = cv.VideoCapture(0)
time.sleep(10.0)

def processImage(orig):
    name = save(orig)
    src = cv.imread(name, cv.CV_8UC1)
    img = prepare(src,orig)
    findContours(img,orig)
    for img in croppedImages:
        print("cropped")
        #predict(img)
      ##  predict(img)


def save(img):
    current = str(time.time())
    name = 'Frames/frame_'+ current +'.png'
    cv.imwrite(name,img)
    return name

def crop(x,y,w,h,img):
    #crop the image using array slices -- it's a NumPy array
    cropped = img[y:y+h, x:x+w]
    croppedImages.append(cropped)

def prepare(img,orig):
    kernel = np.ones((4,4),np.uint8)
    img_gray_u8 = img_as_ubyte(img) 
    ##im_bw = cv.adaptiveThreshold(img_gray_u8, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY , 11, 2)
    edges = cv.Canny(img_gray_u8,50,150,apertureSize = 3)
    cv.imshow("sss",edges)
 
    return edges

def detect(cont, orig):
    # compute the bounding box of the contour and use the
    # bounding box to compute the aspect ratio
    peri = cv.arcLength(cont, True)
    approx = cv.approxPolyDP(cont, 0.04 * peri, True)
    (x, y, w, h) = cv.boundingRect(approx)
    ar = w / float(h)
    # a square will have an aspect ratio that is approximately
    # equal to one, otherwise, the shape is a rectangle
    shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    if shape == "rectangle":
        crop(x,y,w,h,orig)

    return shape

def findContours(img,orig):
    gray_image = cv.convertScaleAbs(img)
    edged = cv.Canny(gray_image, 30, 200)
    img, contours, hierarchy = cv.findContours(edged.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts = sorted(contours, key = cv.contourArea, reverse = True)[:10]
    screenCnt = None
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv.moments(c)
        cX = int((M["m10"] / M["m00"]))
        cY = int((M["m01"] / M["m00"]))
        shape = detect(c,orig)
    
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c = c.astype("int")
        cv.drawContours(orig, [c], -1, (0, 255, 0), 2)        
        cv.putText(orig, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,
            0.5, (255, 255, 255), 2)
        cv.imshow("Image", orig)

def predict(img):
    #cv.imshow("Window", im_bw)
    # resize using opencv
    img_resized = cv.resize(img, (28, 28))
    ############################################################
    # invert image
    im_gray_invert = 255 - img_resized
    #cv.imshow("Window", im_gray_invert)
    ####################################
    im_final = im_gray_invert.reshape(1, 28, 28, 1)
    # the below output is a array of possibility of respective digit
    ans = model.predict(im_final)
    print(ans)
    # choose the digit with greatest possibility as predicted dight
    ans = ans[0].tolist().index(max(ans[0].tolist()))
    print('DNN predicted digit is: ', ans)


def main():
    # loop over the frames from the video stream
    while True:
        try:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            
            #readimage
            frame = cv.imread(".\image.png")
            ##ret, frame = cap.read()
            frame = imutils.resize(frame, width=400)
            # draw the timestamp on the frame
           
            cv.imshow("Window", frame)   
            
            processImage(frame)         
            key = cv.waitKey(1) & 0xFF
            
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
                # do a bit of cleanup
                cv.destroyAllWindows()
                cap.stop()
            elif key == ord("c"): 
                processImage(frame)     
                pass
        except KeyboardInterrupt:
            # do a bit of cleanup
            cv.destroyAllWindows()
            cap.stop()


if __name__ == "__main__":
    main()

