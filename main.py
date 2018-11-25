import time
import threading
from pynput.keyboard import Key, Controller, Listener

class Worker(threading.Thread):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True

    def run(self):
        keyboard = Controller()
        while self.running:
            print('Running')
            keyboard.press(self.repeat_key)
            keyboard.release(self.repeat_key)
            time.sleep(self.interval)

class Repeater():
    def __init__(self, *args, **kwargs):
        self.worker = None
        self.on_off_key = '`'
        self.exit_key = Key.esc
        self.changing_key = False
        self.repeat_key = 'z'
        self.interval = 1

    def change_key(self,key):
        if key != self.on_off_key and key != self.exit_key:
            self.repeat_key = key
            return True
        return False

    def on_press(self,key):        
        if getattr(key,'char',None) == self.on_off_key:  
            self.changing_key = True
        elif self.changing_key:
            self.change_key(key)

        if key == self.exit_key:
            return False
        
    def on_release(self,key):
        if getattr(key,'char',None) == self.on_off_key:
            self.changing_key = False            
            if self.worker:
                self.stop_repeat()
            else:
                self.start_repeat()

    def start_repeat(self):
        print('Start worker')
        self.worker = Worker()
        self.worker.daemon = False
        self.worker.repeat_key = self.repeat_key
        self.worker.interval = self.interval
        self.worker.start()

    def stop_repeat(self):
        print('Stop worker')
        self.worker.running = False
        self.worker = None

    def listen(self):
        # Collect events until released
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    r = Repeater()
    r.listen()    
    