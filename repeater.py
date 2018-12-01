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
        self._interval = 1

    @property
    def running(self):
        return self.worker is not None

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self,value):
        if value > 0:
            self._interval = value
            if self.worker:
                self.worker.interval = value

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
