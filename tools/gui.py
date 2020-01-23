import sys
sys.path.insert(0, '..')
import pages
import tkinter as tk


class TkView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.switch_frame(pages.PageTitle)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()