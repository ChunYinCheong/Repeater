import time
import threading
from pynput.keyboard import Key, Controller, Listener, KeyCode
from repeater import Repeater
from hotkey import Hotkey

if __name__ == "__main__":
    r = Repeater()
    h = Hotkey()
    h.repeater = r
    with Listener(
        on_press=h.on_press,
        on_release=h.on_release) as listener:
        listener.join()
    