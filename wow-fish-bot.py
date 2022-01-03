# -*- coding: utf-8 -*-
# WoW Fish BOT by YECHEZ
# github.com/YECHEZ/wow-fish-bot

import time
import pyautogui
import numpy as np
import cv2
from ewmh import EWMH
import random
from PIL import ImageGrab
from Xlib import X, display

ewmh = EWMH()
lastx = 0
lasty = 0
is_block = False
new_cast_time = 0
recast_time = 40
wait_mes = 0
wowwin = None

display = display.Display()

for win in ewmh.getClientList():
    if win.get_wm_name() == "World of Warcraft":
        wowwin = win


if __name__ == "__main__":
    while True:
        win = ewmh.getActiveWindow()
        if win.get_wm_name() != "World of Warcraft":
            if wait_mes == 5:
                wait_mes = 0
            print("Waiting for World of Warcraft as active window")
            wait_mes += 1
            time.sleep(2)
        else:
            geo = win.get_geometry()
            rect = geo.x, geo.y, geo.width + geo.x, geo.height + geo.y

            if is_block == False:
                lastx = 0
                lasty = 0
                pyautogui.press('1')
                print("Fish on !")
                new_cast_time = time.time()
                is_block = True
                time.sleep(random.uniform(1.5, 3.5))
            else:
                fish_area = (0, rect[3] / 2, rect[2], rect[3])

                img = ImageGrab.grab(fish_area)
                img_np = np.array(img)

                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                h_min = np.array((0, 0, 253), np.uint8)
                h_max = np.array((255, 0, 255), np.uint8)

                mask = cv2.inRange(frame_hsv, h_min, h_max)

                moments = cv2.moments(mask, 1)
                dM01 = moments['m01']
                dM10 = moments['m10']
                dArea = moments['m00']

                b_x = 0
                b_y = 0

                if dArea > 0:
                    b_x = int(dM10 / dArea)
                    b_y = int(dM01 / dArea)
                if lastx > 0 and lasty > 0:
                    if lastx != b_x and lasty != b_y:
                        is_block = False
                        if b_x < 1: b_x = lastx
                        if b_y < 1: b_y = lasty
                        wowwin.set_input_focus(X.RevertToParent, X.CurrentTime)
                        wowwin.configure(stack_mode=X.Above)
                        display.sync()
                        pyautogui.moveTo(b_x, b_y + fish_area[1], 0.3)
                        pyautogui.mouseDown(button='right')
                        time.sleep(random.uniform(0.05, 0.15))
                        pyautogui.mouseUp(button='right')
                        print("Catch !")
                        time.sleep(random.uniform(4, 7))
                lastx = b_x
                lasty = b_y

                if time.time() - new_cast_time > recast_time:
                    print("New cast if something wrong")
                    is_block = False
        if cv2.waitKey(1) == 27:
            break
