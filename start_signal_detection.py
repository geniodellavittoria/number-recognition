import cv2 as cv


def main():
    img = cv.imread("startSignal.png")
    start_hsv = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    hist = cv.calcHist([img], [0, 1], None, [16, 16], [
        0, 180, 0, 256], accumulate=False)
    value = cv.compareHist(hist, hist, cv.HISTCMP_KL_DIV)
    print(value)


if __name__ == "__main__":
    main()
