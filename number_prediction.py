import cv2 as cv
from keras.models import load_model

model = load_model(r'.\\mnist_trained_model.h5')


def init():
    img = cv.imread("subimg.png", cv.COLOR_BGR2GRAY)
    img.shape
    start(img)


def start(img):
    #cv.imshow("Window", im_bw)
    # resize using opencv
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    (thresh, img) = cv.threshold(img_gray,
                                 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    sub_bw = cv.threshold(img, thresh, 255, cv.THRESH_BINARY_INV)[1]

    sliced = img[:, :, 0]
    img_resized = cv.resize(sliced, (28, 28))

    # the below output is a array of possibility of respective digit
    im_final = sub_bw.reshape(1, 28, 28, 1)

    ans = model.predict(im_final)
    print(ans)
    # choose the digit with greatest possibility as predicted dight
    ans = ans[0].tolist().index(max(ans[0].tolist()))
    print('DNN predicted digit is: ', ans)

    # cv.waitKey(0)


if __name__ == "__main__":
    init()
