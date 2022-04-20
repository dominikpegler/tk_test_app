#!/bin/python3

from tkinter.ttk import Frame, Label, Entry, Button
from tkinter import Text, Menu, Tk
from tkinter.font import Font
from tkinter.messagebox import showinfo, showerror, showwarning
from sys import exit
import platform
from queries import (
    load_config,
    get_item,
    get_next_item,
)
from save_drawings import save_pdf, save_dwg

DB = "OE"  # 'SL' or 'OE'
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
FONTS = ["Tahoma", "DejaVu Sans", "Helvetica", "Arial"]
FONTSIZE = 9


def main():
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
            self.entry_field.bind("<Prior>", self.call_next_item)
            self.entry_field.bind("<Up>", self.call_next_item)
            self.entry_field.bind("<Down>", self.call_next_item)
            self.entry_field.bind("<Next>", self.call_next_item)
            self.entry_field.pack()
            self.entry_field.focus_set()
            # entry_field.place(x=80, y=150)

            self.submit_button = Button(self, text="Submit", command=self.call_item)
            self.submit_button.pack(pady=30)
            # submit_button.place(x=80, y=100)

            self.output_field = Label(self)
            self.output_field.pack(pady=30)

            self.download_button = Button(
                self, text="Download PDF + DWG", command=self.download_drawings
            )
            self.download_button.pack(pady=30)

            # load configuration file
            self.call_config()

        # commands
        def not_implemented(self, event=None):
            showinfo("Not implemented", "Function not yet implemented.")

        def show_about(self):
            showinfo("Info", APP_TITLE + " Version " + APP_VERSION + "\n" + SYSTEM_INFO)

        def client_exit(self):
            exit()

        def call_config(self):
            result, content = load_config(DB)
            if result == "Ok":
                self.database_string = content
            elif result == "Err":
                showerror("Error", content, parent=root)
                exit()
            else:
                showwarning("Warning", "Undefined behavior.")

        def download_drawings(self):
            if self.pdf_file == "":
                result_1, msg_1 = "Err", "Kein PDF hinterlegt."
            else:
                result_1, msg_1 = save_pdf(self.pdf_file)
            if self.dwg_file == "":
                result_2, msg_2 = "Err", "Kein DWG hinterlegt."
            else:
                result_2, msg_2 = save_dwg(self.dwg_file)

            if (result_1 == "Ok") & (result_2 == "Ok"):
                showinfo("Info", "Zeichnungen gespeichert!")
            elif (result_1 == "Err") | (result_2 == "Err"):
                showwarning("Hinweis", msg_1 + " " + msg_2, parent=root)
            else:
                print("result_1", result_1)
                print("result_2", result_2)
                showwarning("Warning", "Undefined behavior.")

        def call_item(self, event=None):

            result, content = get_item(self.entry_field.get(), self.database_string, DB)

            self.pdf_file = str(content[3] or "")
            self.dwg_file = str(content[4] or "")

            if result == "Ok":
                self.output_field.config(
                    text=content[0]
                    + "\n\nZeichnung: "
                    + str(content[1])
                    + "\nIndex: "
                    + str(content[2])
                    + "\nBild: "
                    + self.pdf_file
                    + "\nCAD: "
                    + self.dwg_file
                )
                self.output_field.pack()
                self.entry_field.focus_set()

            elif result == "Err":
                showerror("Error", content[0], parent=root)
                exit()

            else:
                showwarning("Warning", "Undefined behavior.")

        def call_next_item(self, event=None):

            if event.keysym in ["Prior", "Next", "Up", "Down"]:

                result, (input, *content) = get_next_item(
                    self.entry_field.get(), event.keysym, self.database_string, DB
                )

                self.pdf_file = str(content[3] or "")
                self.dwg_file = str(content[4] or "")

                if result == "Ok":
                    self.output_field.config(
                        text=content[0]
                        + "\n\nZeichnung: "
                        + str(content[1])
                        + "\nIndex: "
                        + str(content[2])
                        + "\nBild: "
                        + self.pdf_file
                        + "\nCAD: "
                        + self.dwg_file
                    )
                    self.output_field.pack()
                    self.entry_field.delete(0, "end")
                    self.entry_field.insert(0, input)
                    self.entry_field.focus_set()

                elif result == "Err":
                    showerror("Error", content, parent=root)
                    exit()

                else:
                    showwarning("Warning", "Undefined behavior.")

            else:
                content = f"event.keysym kann nur 'Up', 'Down', 'Prior' oder 'Next' sein, ist aber {str(event.keysym)}. Check code!"
                showerror("Error", content, parent=root)
                exit()

    root = Tk()
    if platform.system() == "Windows":
        root.iconbitmap("icon.ico")
    root.geometry(WINDOW_SIZE)
    text = Text(root)
    menu_font = Font(family=FONTS, size=FONTSIZE)
    text.configure(font=menu_font)
    app = Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
