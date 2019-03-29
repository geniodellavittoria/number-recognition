import cv2 as cv
from keras.models import load_model

model = load_model(r'.\\mnist_trained_model.h5')


def getImg():
    # getimgfromSource
    print("not Implmented yet")


def init(logger):
    log = logger


def start(img):
    #cv.imshow("Window", im_bw)
    # resize using opencv
    img_resized = cv.resize(img, (28, 28))
    ############################################################
    # invert image
    im_gray_invert = 255 - img_resized
    #cv.imshow("Window", im_gray_invert)
    ####################################
    print(im_gray_invert.shape)
    im_final = im_gray_invert.reshape(1, 28, 28, 1)
    # the below output is a array of possibility of respective digit
    ans = model.predict(im_final)
    print(ans)
    # choose the digit with greatest possibility as predicted dight
    ans = ans[0].tolist().index(max(ans[0].tolist()))
    print('DNN predicted digit is: ', ans)


if __name__ == "__main__":
    getImg()
