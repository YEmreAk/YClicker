import os
import sys
from threading import Thread
from time import sleep, time
from tkinter import Button, Entry, Frame, IntVar, Label, PhotoImage, StringVar, Tk
from typing import Tuple

from keyboard import add_hotkey, on_press_key, press_and_release, read_hotkey, remove_hotkey, unhook
from mouse import click


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App:

    window: Tk

    def __init__(self, title: str, size: Tuple[int, int]) -> None:
        self.window = Tk()
        self.window.title(title)
        self.window.resizable(False, False)
        self.window.iconphoto(True, PhotoImage(file = resource_path('images/icon.png')))

        App.centerilaze(self.window, *size)

        self.main_frame = Frame(self.window)
        self.main_frame.pack()

        self.__row = 0
        self.__column = 0

        self.__key = ""
        self.__keypress_speed = 1
        self.__mouseclick_speed = 1
        self.__mouseclick_flag = False
        self.__keypress_flag = False
        self.__run_flag = True

        self.__mhotkey = False
        self.__khotkey = False
        
        self.ltitle_label = Label(self.main_frame, text="Mouse", font="Helvatica 10 bold")
        self.mouse_speed_entry = Entry(self.main_frame, width=5, justify="center", textvariable=IntVar(self.main_frame, 10))
        self.mstart_button = Button(self.main_frame, text="Başlat", fg="green", command=self.on_mouse_button_clicked)
        self.mstop_button = Button(self.main_frame, text="Durdur", state="disabled", foreground="red", command=self.on_mouse_button_clicked)
        self.mhotkey_button = Button(self.main_frame, text="Kısayol", foreground="blue", command=self.on_mouse_hotkey_button_clicked)

        self.rtitle_label = Label(self.main_frame, text="Keyboard", font="Helvatica 10 bold")
        self.key_entry = Entry(self.main_frame, width=5, justify="center", textvariable=StringVar(self.main_frame, "a"))
        self.speed_entry = Entry(self.main_frame, width=5, justify="center", textvariable=IntVar(self.main_frame, 10))
        self.start_button = Button(self.main_frame, text="Başlat", fg="green", command=self.on_key_button_clicked)
        self.stop_button = Button(self.main_frame, text="Durdur", state="disabled", command=self.on_key_button_clicked)
        self.hotkey_button = Button(self.main_frame, text="Kısayol", foreground="blue", command=self.on_key_hotkey_button_clicked)

        self.minfo_label = Label(self.main_frame, text="Henüz çalışmıyor", font='Helvatica 9 italic', pady=3)
        self.info_label = Label(self.main_frame, text="Henüz çalışmıyor", font='Helvatica 9 italic', pady=3)
        self.debug_label = Label(self.main_frame, text="", font="Courier 8 italic", pady=3)


        self.add(self.ltitle_label, pady=(10, 0))
        self.add(self.mouse_speed_entry, padx=(10, 0), pady=(10, 0))
        self.add(self.mstart_button, padx=(10, 0), pady=(10, 0))
        self.add(self.mstop_button, padx=(10, 0), pady=(10, 0))
        self.add(self.mhotkey_button, padx=(10, 0), pady=(10, 0))

        self.add_row()
        self.add(self.rtitle_label, pady=(10, 0))
        self.add(self.key_entry, padx=(10, 0), pady=(10, 0))
        self.add(self.speed_entry, padx=(10, 0), pady=(10, 0))
        self.add(self.start_button, padx=(10, 0), pady=(10, 0))
        self.add(self.stop_button, padx=(10, 0), pady=(10, 0))
        self.add(self.hotkey_button, padx=(10, 0), pady=(10, 0))

        self.add_row()
        self.add(self.minfo_label, columnspan=6, padx=(10, 0), pady=(10,0))

        self.add_row()
        self.add(self.info_label, columnspan=6, padx=(10, 0))

        self.add_row()
        self.add(self.debug_label, columnspan=6, padx=(10, 0))

    @staticmethod
    def centerilaze(root: Tk, width: int, height: int):
        # Gets both half the screen width/height and window width/height
        positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
        positionDown = int(root.winfo_screenheight() / 2.5 - height / 2)

        # Positions the window in the center of the page.
        root.geometry(f"{width}x{height}+{positionRight}+{positionDown}")
        root.geometry("+{}+{}".format(positionRight, positionDown))

    def start(self):
        Thread(target=self.key_press_functionality).start()
        Thread(target=self.mouse_click_functionality).start()
        app.window.mainloop()
        self.__run_flag = False

    def add(self, component, **kwargs):
        component.grid(column=self.__column, row=self.__row, **kwargs)
        self.__column += 1

    def add_row(self):
        self.__row += 1
        self.__column = 0

    def on_key_button_clicked(self):

        if not self.__keypress_flag:
            self.__key = self.key_entry.get()
            self.__keypress_speed = int(self.speed_entry.get())
            self.__keypress_flag = True

            self.speed_entry.configure(state="disabled")
            self.key_entry.configure(state="disabled")
            self.start_button.configure(state="disabled")
            self.hotkey_button.configure(state="disabled")
            self.stop_button.configure(state="normal")

            self.info_label.configure(foreground="green")
            self.info_label["text"] = f"{self.__key} tuşuna saniyede {self.__keypress_speed} kere basılacak"
        else:
            self.__keypress_flag = False

            self.speed_entry.configure(state="normal")
            self.key_entry.configure(state="normal")
            self.start_button.configure(state="normal")
            self.hotkey_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

            self.info_label.configure(foreground="darkorange2")
            self.info_label["text"] = f"Tuş basımı iptal edildi"


    def on_mouse_button_clicked(self):
        if not self.__mouseclick_flag:
            self.__mouseclick_speed = int(self.mouse_speed_entry.get())
            self.__mouseclick_flag = True

            self.mouse_speed_entry.configure(state="disabled")
            self.mstart_button.configure(state="disabled")
            self.mhotkey_button.configure(state="disabled")
            self.mstop_button.configure(state="normal")

            self.minfo_label.configure(foreground="green")
            self.minfo_label["text"] = f"Sol tuşa saniyede {self.__mouseclick_speed} kere basılacak"
        else:
            self.__mouseclick_flag = False

            self.mouse_speed_entry.configure(state="normal")
            self.mstart_button.configure(state="normal")
            self.mhotkey_button.configure(state="normal")
            self.mstop_button.configure(state="disabled")

            self.minfo_label.configure(foreground="darkorange2")
            self.minfo_label["text"] = "Mouse basımı iptal edildi"


    def set_hotkey_bg(self, hotkey_for: str):

        def set_mouse_hotkey():
            self.minfo_label["text"] = "Herhangi bir kısayola basın, iptal için ESC"
            hotkey = read_hotkey()
            if hotkey == "esc":
                self.minfo_label.configure(foreground="darkorange2")
                self.minfo_label["text"] = "Kısayol kaldırıldı"
                if self.__mhotkey:
                    remove_hotkey(self.__mhotkey)
            else:
                self.__mhotkey = add_hotkey(hotkey, self.on_mouse_button_clicked, suppress=True)
                self.minfo_label.configure(foreground="blue")
                self.minfo_label["text"] = f"{hotkey} kısayolu atandı"

        def set_key_hotkey():
            self.info_label["text"] = "Herhangi bir kısayola basın, iptal için ESC"
            hotkey = read_hotkey()
            if hotkey == "esc":
                self.info_label.configure(foreground="darkorange2")
                self.info_label["text"] = "Kısayol kaldırıldı"
                if self.__khotkey:
                    remove_hotkey(self.__mhotkey)
            else:
                self.__keypress_hotkey = hotkey
                self.__khotkey = add_hotkey(hotkey, self.on_key_button_clicked, suppress=True)
                self.info_label.configure(foreground="blue")
                self.info_label["text"] = f"{hotkey} kısayolu atandı"

        Thread(target=set_mouse_hotkey if hotkey_for == "mouse" else set_key_hotkey).start()


    def on_mouse_hotkey_button_clicked(self):
        self.set_hotkey_bg("mouse")

    def on_key_hotkey_button_clicked(self):
        self.set_hotkey_bg("key")

    def key_press_functionality(self):
        next_time = 0
        last_time = time()
        while self.__run_flag:
            current_time = time()
            if self.__keypress_flag and self.__key and current_time > next_time:
                try:
                    press_and_release(self.__key)
                    passed_time = current_time - last_time
                    last_time = current_time
                    self.debug_label["text"] = f"{self.__key:5} tuşuna {passed_time:.3f} içinde tıklandı"
                    next_time = current_time + 1 / self.__keypress_speed
                except ValueError:
                    self.info_label.configure(foreground="red")
                    self.info_label["text"] = f"`{self.__key}` tuşu geçersiz"
            sleep(min([next_time - current_time, 0.3]) if next_time > current_time else 0.3)


    def mouse_click_functionality(self):
        next_time = 0
        last_time = time()
        while self.__run_flag:
            current_time = time()
            if self.__mouseclick_flag and current_time > next_time:
                click("left")
                passed_time = current_time - last_time
                last_time = current_time
                next_time = current_time + 1 / self.__mouseclick_speed
                self.debug_label["text"] = f"{'Sol':5} tuşuna {passed_time:.3f} içinde tıklandı"
            sleep(min([next_time - current_time, 0.3]) if next_time > current_time else 0.3)

app = App("YClicker", (440, 180))
app.start()
