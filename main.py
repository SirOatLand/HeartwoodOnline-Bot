import cv2 as cv
import numpy as np
from time import time, sleep
from windowcapture import WindowCapture
from detection import Detection
from HsvFilter import HsvFilter
from bot import MovementHandler


coal_needles = ['./assets/big_coal1_hsv.jpg', './assets/big_coal2_hsv.jpg', './assets/big_coal3_hsv.jpg']
tin_needles = ['./assets/big_tin1_hsv.jpg', './assets/big_tin2_hsv.jpg']
hsvfilter_coal = HsvFilter(0, 141, 123, 15, 236, 251, 145, 0, 147, 0)
hsvfilter_tin = HsvFilter(11, 0, 0, 98, 255, 132, 255, 0, 62, 14)

# initialize the WindowCapture class
screen_w = 1024
screen_h = 768
wincap = WindowCapture('Heartwood Online', screen_w, screen_h)

DEBUG = True

if __name__ == "__main__":

    # choose needles, hsvfilter, and threshold
    needles = tin_needles
    hsvfilter = hsvfilter_tin
    threshold = 0.7

    # load the detector
    bot_detector = Detection(needles, hsvfilter, threshold)

    # initialize bot class
    bot = MovementHandler(screen_w, screen_h)

    wincap.start()
    bot_detector.start()
    #bot.start()
    while(True):
        begin_time = time()
        bot.update_screen_relative_pos(wincap.get_screen_position((screen_w, screen_h)))
        
        if wincap.get_screenshot() is not None:
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
        
        screenshot = bot_detector.update(screenshot)
        for rect in bot_detector.rectangles:
            if rect is not None :
                if len(rect) > 0 :
                    bot.update_destination(rect)
                    screenshot = bot_detector.visions[0].draw_rectangles(bot_detector.screenshot, rect, bot.find_closest())
                else:
                    bot.clear_destinations()

        print(bot.find_closest())
        if bot.find_closest() is not None:
            obj_x, obj_y, w, h = bot.find_closest()
            bot.move_towards_destination(obj_x, obj_y)

        print('FPS - {}'.format(1 / (time()-begin_time)))
        cv.imshow('All Seeing Eye', screenshot)
        key = cv.waitKey(1)

        if key == ord('q'):
            wincap.stop()
            bot_detector.stop()
            bot.stop()
            cv.destroyAllWindows()
            break

    print('Done.')