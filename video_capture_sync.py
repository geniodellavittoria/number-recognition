from picamera import PiCamera
from time import sleep
import datetime

camera = PiCamera()


def main():
    camera.resolution = (1280, 720)
    camera.framerate = 40
    camera.iso = 800
    camera.shutter_speed = 500
    camera.start_recording('video_40_800_500.h264')
    for i in range(35):
        print(i)
        sleep(1)
    camera.stop_recording()
    camera.stop_preview()


if __name__ == "__main__":
    main()
