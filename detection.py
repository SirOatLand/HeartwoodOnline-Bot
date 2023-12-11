from mss import mss
import cv2
from PIL import Image
import numpy as np
from time import time, sleep
from vision import Vision
from HsvFilter import HsvFilter
import windowcapture as wc 
import pyautogui
from threading import Thread, Lock


class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []

    # properties
    needles = []
    visions = []
    hsvfilter = None
    screenshot = None
    threshold = None

    def __init__(self, needle_img_paths, hsvfilter, threshold):
        # create a thread lock object
        self.lock = Lock()
        # load detector properties
        for img in needle_img_paths:
            self.needles.append(img)
            self.visions.append(Vision(img))
        self.hsvfilter = hsvfilter
        self.threshold = threshold
        

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = self.visions[0].apply_hsv_filter(screenshot, self.hsvfilter)
        self.lock.release()
        return self.screenshot

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = []
                for vision in self.visions:
                    #print(f"{vision} - {vision.find(self.screenshot, self.threshold)}")
                    rectangles.append(vision.find(self.screenshot, self.threshold))
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()