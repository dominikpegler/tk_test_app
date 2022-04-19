#!/bin/python3

from tkinter.ttk import Frame, Label, Entry, Button
from tkinter import Text, Menu, Tk
from tkinter.font import Font
from tkinter.messagebox import showinfo, showerror
import platform
from queries_sqlite import get_item # from queries_oe im...

APP_TITLE = "ProLite App"
APP_VERSION = "0.0.1"
WINDOW_SIZE = "800x600"
SYSTEM_INFO = (
    "\nHostname: "
    + platform.node()
    + "\n\n"
    + "System: "
    + platform.system()
    + " ("
    + str(platform.architecture()[0])
    + ")"
    + "\n\n"
    + "Architecture: "
    + platform.machine()
)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.init_window()

    # layout
    def init_window(self):
        self.master.title(APP_TITLE)
        self.pack(fill="both", expand=1, pady=30)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Open", command=self.not_implemented)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label="Import", command=self.not_implemented)
        menu.add_cascade(label="Edit", menu=edit)

        help = Menu(menu, tearoff=0)
        help.add_command(label="?", command=self.show_about)
        menu.add_cascade(label="Help", menu=help)

        self.entry_field = Entry(self)
        self.entry_field.bind("<Return>", self.call_item)
        self.entry_field.pack()
        # entry_field.place(x=80, y=150)

        self.submit_button = Button(self, text="Submit", command=self.call_item)
        self.submit_button.pack(pady=30)
        # submit_button.place(x=80, y=100)

        self.output_field = Label(self)

    # commands
    def not_implemented(self, event=None):
        showerror("Not implemented", "Function not yet implemented.")

    def show_about(self):
        showinfo("Info", APP_TITLE + " Version " + APP_VERSION + "\n" + SYSTEM_INFO)

    def client_exit(self):
        exit()

    def call_item(self, event=None):
        item_info = get_item(self.entry_field.get())
        self.output_field.config(text=item_info)
        self.output_field.pack()


root = Tk()
if platform.system() == "Windows":
    root.iconbitmap("icon.ico")
root.geometry(WINDOW_SIZE)
text = Text(root)
menu_font = Font(family=["Tahoma", "DejaVu Sans", "Helvetica", "Arial"], size=9)
text.configure(font=menu_font)
app = Window(root)
root.mainloop()
