import pyperclip
import ctypes
import time
import sys

from utils import *
from ui.main_window import MainWindow
from ui.first_launch import FirstLaunch
from ctypes import wintypes, get_last_error
from termcolor import colored
from PyQt6.QtWidgets import QApplication

import win32con
import win32api

WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_GETLASTINPUTINFO = 0x0002

APP = None
WINDOW = None

def close():
    global APP, WINDOW
    print(colored("Closing UI.", "red"))

def get_started_callback(model: str, lang: str):
    global APP, WINDOW

    set_lang(lang)
    set_model(model)
    APP.quit()

    sys.exit(0)

def launch(selected_text: str):
    global APP, WINDOW
    if not APP:
        APP = QApplication(sys.argv)

    if not WINDOW:
        if check_first_launch():
            WINDOW = FirstLaunch(get_started_callback=get_started_callback, close_callback=lambda: sys.exit(0))
            WINDOW.show()
            print(colored("Launched First Launch.", "green"))
        else:
            WINDOW = MainWindow(selected_text=selected_text, close_callback=close)
            WINDOW.show()
            print(colored("Launched UI.", "green"))
    else:
        print(colored("Launched UI.", "green"))
        WINDOW.selected_text = selected_text
        WINDOW.show()

    APP.processEvents()

def get_selected_text():
    """
    Gets selected text by simulating Ctrl+C and reading clipboard
    """

    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(ord('C'), 0, 0, 0)
    win32api.keybd_event(ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(0.1)

    return pyperclip.paste()

def handle_control_space():
    """
    Function called when Control + Space is pressed.
    """
    selected_text = get_selected_text()
    launch(selected_text)

HOTKEYS = [
    {
        "keys": (win32con.VK_SPACE, win32con.MOD_CONTROL),
        "command": handle_control_space
    },
    {
        "keys": (ord('Q'), win32con.MOD_CONTROL | win32con.MOD_ALT),
        "command": lambda: sys.exit(0)
    }
]

for i, h in enumerate(HOTKEYS):
    vk, modifiers = h["keys"]
    if not ctypes.windll.user32.RegisterHotKey(None, i, modifiers, vk):
        error_code = get_last_error()
        print(colored(f"Unable to register id {i} for hotkey {vk}. Error code: {error_code}", "red"))
    else:
        print(colored(f"Registered Hotkey {i} successfully.", "green"))

try:
    msg = wintypes.MSG()
    while True:
        if ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == win32con.WM_HOTKEY:
                try:
                    HOTKEYS[msg.wParam]["command"]()
                except Exception as e:
                    print(colored(f"Error handling hotkey: {e}", "red"))
            try:
                ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
            except Exception as e:
                print(colored(f"Error dispatching message: {e}", "red"))
                continue

        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    for i, _ in enumerate(HOTKEYS):
        ctypes.windll.user32.UnregisterHotKey(None, i)
    print("Cleaned up hotkeys.")
