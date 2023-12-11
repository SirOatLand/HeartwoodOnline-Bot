import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from threading import Thread, Lock

class WindowCapture:

    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    def __init__(self, window_title, width, height):
        # create a thread lock object
        self.lock = Lock()

        self.window_title = window_title
        self.width = width
        self.height = height
        self.hwnd = win32gui.FindWindow(None, self.window_title)

    def get_screenshot(self):
        try:
            hwndDC = win32gui.GetWindowDC(self.hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()

            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, self.width, self.height)

            saveDC.SelectObject(saveBitMap)

            result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 3)

            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)

            image = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1)

            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwndDC)

            if result == 1:
                # PrintWindow Succeeded
                return image
            else:
                return None
        except Exception as e:
            print(f"Exception occurred: {e}")
            return None

    def save_capture(self, filename):
        image = self.get_screenshot()
        if image:
            image.save(filename)
            print(f"Screenshot saved as {filename}")
        else:
            print("Failed to capture window.")
    
    def get_screen_position(self, screenshot_pos):
        window_rect = win32gui.GetWindowRect(self.hwnd)
        
        screen_x = window_rect[0] #+ screenshot_pos[0]
        screen_y = window_rect[1] #+ screenshot_pos[1]

        return (screen_x, screen_y)
    
    # threading methods

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()

# import cv2 as cv
# import numpy as np
# from time import time

# if __name__ == "__main__":
#     wincap = WindowCapture('Heartwood Online', 800, 600)
#     wincap.run()

#     while True:
#         begin_time = time()
#         screenshot = wincap.get_screenshot()
#         screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
#         cv.imshow('All Seeing Eye', screenshot)
#         key = cv.waitKey(1)
#         print('FPS - {}'.format(1 / (time()-begin_time)))
#         if key == ord('q'):
#             wincap.stop()
#             cv.destroyAllWindows()
#             break