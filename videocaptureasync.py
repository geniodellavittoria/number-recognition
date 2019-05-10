# file: videocaptureasync.py
import datetime
import logging as log
import threading
from time import sleep

import cv2
from picamera import PiCamera


class VideoCaptureAsync:
    # def __init__(self, src=0):
        # path = 'C:/Users/tbolz/Desktop/videos/video_40_ss_auto.h264'
        # log.info("init with"+path)
        # self.cap = cv2.VideoCapture(path)
        # self.src = src
        # self.grabbed, self.frame = self.cap.read()
        # self.started = False
        # self.read_lock = threading.Lock()

    def __init__(self, src=0, width=1280, height=720):
        self.src = src
        self.cap = PiCamera()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.framerate = 50
        self.grabbed, self.frame = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def start(self):
        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            grabbed, frame = self.cap.read()
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()
