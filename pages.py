import tools.gui as gui
import tools.clientinput as ci
import tkinter as tk
if ci.is_win():
	import winsound
from PIL import Image, ImageTk


FONT_TITLE_MAIN = 'Fixedsys 40 bold underline'
FONT_TITLE_SECOND = 'Fixedsys 20 bold'
FONT_BUTTON = 'verdana 15'


class PageTitle(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#self.winfo_toplevel().geometry('500x190')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().title('GD Level Transfer Tool v1')
		if ci.is_win():
			winsound.PlaySound('media/power.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
		tk.Label(self, text='Level Transfer Tool', fg='white', bg='black', 
			font=FONT_TITLE_MAIN).grid(row=0, column=0, columnspan=2)
		self.main_canvas = tk.Canvas(self, width=300, height=300, background='black')
		self.main_canvas.grid(row=1, column=0, columnspan=2)
		self.main_canvas_photo_resize = Image.open('media/noway.png').resize((300, 300), Image.ANTIALIAS)
		self.main_canvas_photo = ImageTk.PhotoImage(self.main_canvas_photo_resize)
		self.main_canvas.create_image(0, 0, image=self.main_canvas_photo, anchor='nw')
		tk.Button(self, text='Upload Level', font=FONT_BUTTON, 
			command=lambda: master.switch_frame(PageUpload)).grid(row=2, column=0, sticky='W')
		tk.Button(self, text='Download Level', font=FONT_BUTTON,
			command=lambda: master.switch_frame(PageDownload)).grid(row=2, column=1, sticky='E')
		self.winfo_toplevel().grid_rowconfigure(2, minsize=200)


class PageUpload(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#self.winfo_toplevel().geometry('500x190')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().title('Upload your Level')
		if ci.is_win():
			winsound.PlaySound('media/sakupen.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)
		self.upload_canvas = tk.Canvas(self, width=300, height=300, background='black')
		self.upload_canvas.grid(row=1, column=0, rowspan=2)
		tk.Label(self, text='Upload Level', fg='white', bg='black', 
			font=FONT_TITLE_SECOND).grid(row=0, column=0)
		tk.Button(self, text='>', font=FONT_BUTTON, 
			command=lambda: master.switch_frame(PageTitle)).grid(row=3, column=1)
		self.upload_entry = tk.Entry(self)
		tk.upload_canvas.create_window(0, 0, window=self.upload_entry)
