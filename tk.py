import tkinter as tk
from main import Repeater, Hotkey

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.key_label = tk.Label(self)
        self.key_label["text"] = "Key: "
        self.key_label.pack()
        self.interval_label = tk.Label(self)
        self.interval_label["text"] = "Interval: "
        self.interval_label.pack()

        self.on_off_button = tk.Button(self)
        self.on_off_button["text"] = "On / Off"
        self.on_off_button["command"] = self.on_off
        self.on_off_button.pack(side="top")

    def on_off(self):
        self.repeater.switch()
        self.refresh()

    def refresh(self):
        self.on_off_button["text"] = "On" if self.repeater.running else "Off"
        self.key_label["text"] = f"Key: {self.repeater.repeat_key}"
        self.interval_label["text"] = f"Interval: {self.repeater.interval}" 

root = tk.Tk()
app = Application(master=root)

r = Repeater()
h = Hotkey(repeater=r)
with Listener(
    on_press=h.on_press,
    on_release=h.on_release) as listener:
    listener.join()
app.repeater = r
app.refresh()


app.mainloop()