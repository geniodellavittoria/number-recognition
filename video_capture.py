import datetime
from time import sleep

from picamera import PiCamera
from videocaptureasync import VideoCaptureAsync

cam = VideoCaptureAsync()


def main():
    frame_rate = 50
    cam.cap.start_recording('video_' + frame_rate + '.h264')
    for i in range(5):
        print(i)
        sleep(1)
    cam.cap.stop_recording()
    cam.cap.stop_preview()


if __name__ == "__main__":
    main()
