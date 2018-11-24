import time
import threading
from pynput.keyboard import Key, Controller, Listener

class Worker(threading.Thread):    
    running = True

    def run(self):
        keyboard = Controller()
        while self.running:
            print('Running')
            keyboard.press(self.repeat_key)
            keyboard.release(self.repeat_key)
            time.sleep(self.interval)


def main():
    worker = None
    on_off_key = '`'
    exit_key = Key.esc
    changing_key = False

    repeat_key = 'z'
    interval = 1

    def change_key(key):
        if key != on_off_key and key != exit_key:
            nonlocal repeat_key
            repeat_key = key
            return True
        return False

    def on_press(key):        
        print('{0} pressed'.format(key))
        nonlocal worker
        if getattr(key,'char',None) == on_off_key:  
            nonlocal changing_key
            changing_key = True
        elif changing_key:
            change_key(key)

        if key == exit_key:
            return False
        
    def on_release(key):
        print('{0} release'.format(key))
        nonlocal worker
        if getattr(key,'char',None) == on_off_key:
            nonlocal changing_key
            changing_key = False            
            if worker and worker.is_alive():
                print('Stop worker')
                worker.running = False
            else:
                print('Start worker')
                worker = Worker()
                worker.daemon = False
                worker.repeat_key = repeat_key
                worker.interval = interval
                worker.start()


    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()