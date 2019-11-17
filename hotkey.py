import time
import threading
from pynput.keyboard import Key, Controller, Listener, KeyCode

class Hotkey():
    def __init__(self, *args, **kwargs):
        self.repeater = kwargs.get("repeater",None)
        self.changing_key = False
        #self.on_off_key = KeyCode.from_vk(192) # "`" Key`
        self.on_off_key = KeyCode.from_char('`')
        self.exit_key = Key.esc
        self.faster_key = Key.page_down
        self.slower_key = Key.page_up
    
    def change_key(self,key):
        if self.repeater:
            if key not in [self.on_off_key, 
                    self.exit_key, self.faster_key,
                    self.slower_key]:
                self.repeater.repeat_key = key

    def on_press(self,key):
        if key == self.exit_key:
            return False
        if key == self.faster_key:
            self.repeater.interval -= 0.1
            print(self.repeater.interval)
            return
        if key == self.slower_key:
            self.repeater.interval += 0.1
            print(self.repeater.interval)
            return
        if key == self.on_off_key:  
            self.changing_key = True
        elif self.changing_key:
            self.change_key(key)
        
    def on_release(self,key):
        if key == self.on_off_key:
            self.changing_key = False
            if self.repeater:
                self.repeater.switch()

    