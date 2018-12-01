import time
import threading
from pynput.keyboard import Key, Controller, Listener, KeyCode

class Worker(threading.Thread):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True

    def run(self):
        keyboard = Controller()
        while self.running:
            print('Running')
            keyboard.press(self.repeat_key)
            time.sleep(0.02)
            keyboard.release(self.repeat_key)
            time.sleep(self.interval)

class Repeater():
    def __init__(self, *args, **kwargs):
        self.worker = None
        self.repeat_key = 'z'
        self.interval = 1

    def switch(self):      
        if self.worker:
            self.stop_repeat()
        else:
            self.start_repeat()

    def start_repeat(self):
        if self.worker:
            self.stop_repeat()
        print('Start worker')
        self.worker = Worker()
        self.worker.daemon = False
        self.worker.repeat_key = self.repeat_key
        self.worker.interval = self.interval
        self.worker.start()

    def stop_repeat(self):
        if self.worker:
            print('Stop worker')
            self.worker.running = False
            self.worker = None

class Hotkey():
    def __init__(self, *args, **kwargs):
        self.changing_key = False
        #self.on_off_key = KeyCode.from_vk(192) # "`" Key`
        self.on_off_key = KeyCode.from_char('`')
        self.exit_key = Key.esc
    
    def change_key(self,key):
        if self.repeater:
            if key != self.on_off_key and key != self.exit_key:
                self.repeater.repeat_key = key

    def on_press(self,key):
        if key == self.exit_key:
            return False      
        if key == self.on_off_key:  
            self.changing_key = True
        elif self.changing_key:
            self.change_key(key)
        
    def on_release(self,key):
        if key == self.on_off_key:
            self.changing_key = False
            if self.repeater:
                self.repeater.switch()

if __name__ == "__main__":
    r = Repeater()
    h = Hotkey()
    h.repeater = r
    with Listener(
        on_press=h.on_press,
        on_release=h.on_release) as listener:
        listener.join()
    