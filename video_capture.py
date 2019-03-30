from picamera import PiCamera
from time import sleep

camera = PiCamera()


def main():
    camera.start_preview()
    camera.start_recording('/home/pi/video.h264')
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()


if __name__ == "__main__":
    main()
