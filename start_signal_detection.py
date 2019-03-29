import cv2 as cv
import numpy as np


def main():
    img = cv.imread("startSignal.png")
    start_hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    hist = cv.calcHist([img], [0, 1], None, [16, 16], [
        0, 180, 0, 256], accumulate=False)
    value = cv.compareHist(hist, hist, cv.HISTCMP_KL_DIV)
    # input img
    image_hsv = 0
    detection(start_hsv, image_hsv, hist)
    print(value)


def detection(start_hsv, image_hsv, hist_start):
    result = np.ones((image_hsv.shape[0], image_hsv.shape[1]))
    start_x = start_hsv.shape[0] // 2 + 1
    start_y = start_hsv.shape[1] // 2 + 1
    step = 1
    delta_x = start_hsv.shape[0] // 2
    delta_y = start_hsv.shape[1] // 2
    for i in range(start_x, image_hsv.shape[0]-start_x, step):
        for j in range(start_y, image_hsv.shape[1]-start_y, step):
            sub_img = image_hsv[i-delta_x:i+delta_x, j-delta_y:j+delta_y, :]
            hist_image = cv.calcHist([sub_img], channels=[0, 1], mask=None, histSize=[
                16, 16], ranges=[0, 180, 0, 256])
            result[i, j] = cv.compareHist(
                hist_start, hist_image, cv.HISTCMP_BHATTACHARYYA)
    print('done')
    print(np.min(result))
    print(np.max(result))
    result_img = 255.0 - result * 255.0
    cv.imshow("result", result_img)


if __name__ == "__main__":
    main()
