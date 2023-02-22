import random
import time
import tkinter as tk
from multiprocessing import Process

import pyautogui
import win32con
import win32gui
import win32api
from loguru import logger
from PIL import Image, ImageTk

X, Y = None, None


def run_wechat():
    hwnd = win32gui.FindWindow(None, "企业微信")
    # https://blog.csdn.net/jr126/article/details/109647187
    # https://mhammond.github.io/pywin32/objects.html
    # https://cloud.tencent.com/developer/article/1741061
    if hwnd != 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
    else:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    win32api.SetCursorPos([left + 34, top + 42])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
    )
    time.sleep(3)
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def mouse_move():
    global X, Y
    pyautogui.FAILSAFE = False
    screenWidth, screenHeight = pyautogui.size()
    current_x, current_y = pyautogui.position()
    if (current_x == X and current_y == Y) or ((None, None) == (X, Y)):
        random_x, random_y = (
            random.randint(0, pyautogui.size().width),
            random.randint(0, pyautogui.size().height),
        )
        logger.info(
            f"开始随机移动鼠标, 原来的鼠标位置 x:{X}, y:{Y}, 现在的鼠标位置 x:{random_x}, y:{random_y}"
        )
        pyautogui.moveTo(random_x, random_y, 1)
        X, Y = random_x, random_y
        return True
    else:
        logger.info(
            f"不需要移动鼠标，原来的鼠标位置 x:{X}, y:{Y}, 现在的鼠标位置 x:{current_x}, y:{current_y}"
        )
        X, Y = current_x, current_y


# def mouse_click(x, y):
#     pyautogui.click(x=x, y=y, interval=1)


def start(seconds):
    while True:
        mouse_move() and run_wechat()
        time.sleep(seconds)


def lock_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.90)
    root.bind_all("<Control-z>", lambda event: root.destroy())
    photo = ImageTk.PhotoImage(
        file=r"D:\备份资料\个人资料\Python\Python小工具\wechat_online\lock.png"
    )
    tk.Label(root, image=photo).pack()
    # tk.Button(root, text="点击执行回调函数", command=root.quit).pack()
    # pass_input = tk.Text(root, width="40", height="3")
    # pass_input.pack()
    root.mainloop()


if __name__ == "__main__":
    p = Process(target=start, args=(10,))
    p.daemon = True
    p.start()
    lock_screen()
