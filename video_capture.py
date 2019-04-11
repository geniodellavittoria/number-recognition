from picamera import PiCamera
from time import sleep
import datetime

camera = PiCamera()


def main():
    camera.rotation = 180
    camera.resolution = (720, 480)
    camera.framerate = 15
    camera.start_preview()
    time = datetime.time
    camera.start_recording('video_' + time + '.h264')
    for i in range(5):
        print(i)
        sleep(1)
    camera.stop_recording()
    camera.stop_preview()


if __name__ == "__main__":
    main()
