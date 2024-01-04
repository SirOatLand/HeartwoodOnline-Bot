from threading import Thread, Lock
import keyboard
import pyautogui
import cv2 as cv
import numpy as np
from time import time, sleep
import math
import win32api, win32con

key_a = 0x41
key_d = 0x44
key_w = 0x57
key_s = 0x53
key_1 = 0x31
key_2 = 0x32
key_3 = 0x33
key_4 =	0x34
key_5 = 0x35

class MobBot:

    stopped = True
    found = False

    bigscreen = (1920, 1080)
    screen_w = None
    screen_h = None
    screen_pos = None

    destinations = []
    character_x = None
    character_y = None

    move_anyset = 0

    def __init__(self, screen_w, screen_h):
        self.lock = Lock()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.character_x = self.screen_w // 2
        self.character_y = self.screen_h // 2

    def calculate_center(self, obj):
        obj_center_x = obj[0] + (obj[2] // 2 if len(obj) > 2 else 0)  # Calculate object center x if obj[2] exists
        obj_center_y = obj[1] + (obj[3] // 2 if len(obj) > 3 else 0)  # Calculate 

        return (obj_center_x, obj_center_y)

    def calculate_distance(self, obj1, obj2):
        x1, y1 = self.calculate_center(obj1)
        x2, y2 = self.calculate_center(obj2)

        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    def update_screen_relative_pos(self, screen_pos):
        self.lock.acquire()
        self.screen_pos = screen_pos
        self.lock.release()
 

    def attack_towards_destination(self, object_center_x, object_center_y):   

        object_center_y += 100

        distance_to_target = self.calculate_distance((self.character_x, self.character_y), self.find_closest())
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

        distance_to_click = 300


        if distance_to_target <= distance_to_click:
            click_x, click_y = self.screen_pos
            click_x, click_y = (object_center_x + click_x, object_center_y + click_y)

        elif distance_to_target > distance_to_click:
            click_x, click_y = self.screen_pos
            click_x += self.character_x 
            click_y += self.character_y
            
            # Calculate angle between character and target
            angle = math.atan2(object_center_y - self.character_y, object_center_x - self.character_x)
            
            # Calculate the click position offsets from the shooter
            offset_x = int(distance_to_click * math.cos(angle))
            offset_y = int(distance_to_click * math.sin(angle))

            click_x += offset_x
            click_y += offset_y

        win32api.SetCursorPos((click_x, click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.keybd_event(key_1, 0, 0, 0)
        sleep(0.05)
        win32api.keybd_event(key_2, 0, 0, 0)
        sleep(0.05)
        win32api.keybd_event(key_3, 0, 0, 0)
        sleep(0.05)
        win32api.keybd_event(key_1, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(key_2, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(key_3, 0, win32con.KEYEVENTF_KEYUP, 0)
        return

    def update_destination(self, destinations):
        self.lock.acquire()
        self.destinations = destinations
        self.lock.release()

    def clear_destinations(self):
        self.lock.acquire()
        self.destinations = []
        self.lock.release()

    def find_closest(self):
        closest_distance = float('inf')
        closest_coordinate = None

        self.lock.acquire()
        for coord in self.destinations:
            obj_center_x, obj_center_y = self.calculate_center(coord)
            distance = math.sqrt((obj_center_x - self.character_x)**2 + (obj_center_y - self.character_y)**2)

            if distance < closest_distance:
                closest_distance = distance
                closest_coordinate = coord

        self.lock.release()
        return closest_coordinate
        

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.find_closest() is not None:
                obj_x, obj_y, w, h = self.find_closest()

                self.lock.acquire()
                self.move_towards_destination(obj_x, obj_y)
                self.lock.release()
