#!/bin/python3

from ast import AnnAssign
from tkinter import Text, Frame, Menu, Label, Tk
from tkinter.font import Font
import subprocess
import re


#BG_COLOR = "#9966ff"
BG_COLOR = "#fff"
BG_COLOR_2 = "#101a1f"


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.init_window()  

    # layout
    def init_window(self):
        self.master.title("TestApp")

        self.pack(fill="both", expand=1)

        menu = Menu(self.master, bg=BG_COLOR)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label="Open")
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", font=myFont, menu=file)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label="Import", command=self.import_csv)
        menu.add_cascade(label="Edit", font=myFont, menu=edit)

        help = Menu(menu, tearoff=0)
        help.add_command(label="?")
        help.add_command(label="Info")
        menu.add_cascade(label="Help", font=myFont, menu=help)

    # commands
    def import_csv(self):
        text = Label(self, text="Hey there!", bg=BG_COLOR)
        text.pack()

    def client_exit(self):
        exit()

    def clean_output(self,text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        result = ansi_escape.sub('', text)
        return result

    def print_status(self):
        sh_cmd = "expressvpn status"
        process = subprocess.Popen(sh_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode("utf-8")
        output = self.clean_output(output)
        text = Label(self, text=output, bg=BG_COLOR, justify="center")
        text.pack()


root = Tk()
root.geometry("800x600")
text = Text(root)
myFont = Font(family="DejaVu Sans", size=10)
text.configure(font=myFont)
app = Window(root)
status = app.print_status()
root.configure(bg=BG_COLOR_2)
app.configure(bg=BG_COLOR_2)
root.mainloop()
