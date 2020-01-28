import tools.gui as gui
import tools.clientinput as ci
import tools.gdlevelclient as glc
import server.clienttoserver as cts
import server.leveldata as ld
import tkinter as tk
from PIL import Image, ImageTk


FONT_TITLE_MAIN = 'Fixedsys 40 bold underline'
FONT_TITLE_SECOND = 'Fixedsys 20 bold'
FONT_TITLE_DESC = 'system 16 bold underline'
FONT_TITLE_ACTION = 'system 20 bold'
FONT_BUTTON_SMALL = 'verdana 10'
FONT_BUTTON = 'verdana 15'


MUSIC_POWER = 'media/power.wav'
MUSIC_SAKUPEN = 'media/sakupen.wav'
MUSIC_FALLING = 'media/falling.wav'


GLOBAL_MUSIC = True

# Unused "Loading" label code (maybe for future update)
"""
prev = '/'
self.label_searching = tk.Label(self, text='Loading level... ' + prev, fg='white', bg='black',
	font=FONT_BUTTON)
self.label_searching.grid(row=2, column=0, padx=100, pady=100)
while not game_save.status:
	time.sleep(0.5)
	gui.loading(self.label_searching, game_save.status, prev)
"""


class PageTitle(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.winfo_toplevel().geometry('700x420')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().configure(bg='black')
		self.winfo_toplevel().title('GD Level Transfer Tool v1')
		gui.sound(MUSIC_SAKUPEN)
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
		self.winfo_toplevel().geometry('500x330')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().configure(bg='black')
		self.winfo_toplevel().title('Upload your Level')
		gui.sound(MUSIC_POWER)
		#self.upload_canvas = tk.Canvas(self, width=300, height=300, background='black')
		#self.upload_canvas.grid(row=1, column=0, rowspan=2)
		tk.Label(self, text='Upload Level', fg='white', bg='black', 
			font=FONT_TITLE_SECOND).grid(row=0, column=1, padx=50)
		tk.Button(self, text='Back', font=FONT_BUTTON_SMALL, 
			command=lambda: master.switch_frame(PageTitle)).grid(row=0, column=2)
		
		self.button_scan = tk.Button(self, text='Load Topmost Level', font=FONT_BUTTON, 
			command=lambda: self.scan(self.button_scan))
		self.button_scan.grid(row=2, column=1, pady=100)

	def clear_wid(self, obj):
		if isinstance(obj, list):
			for b in obj:
				try:
					b.grid_forget()
				except:
					pass
		else:
			obj.grid_forget()

	def scan(self, button):
		self.clear_wid(button)
		game_save = glc.GameSave()
		if game_save.top_level():
			self.label_name = tk.Label(self, text='Name', fg='white', bg='black', 
				font=FONT_TITLE_DESC)
			self.label_name.grid(row=1, column=1)
			self.label_level_name = tk.Label(self, text=game_save.top_level().name, fg='white', bg='black', 
			font=FONT_BUTTON)
			self.label_level_name.grid(row=2, column=1)
			self.label_desc = None
			self.label_level_desc = None
			self.label_length = None
			self.label_level_length = None
			if game_save.top_level().desc:
				self.label_desc = tk.Label(self, text='Description', fg='white', bg='black', 
					font=FONT_TITLE_DESC)
				self.label_desc.grid(row=3, column=1)
				self.label_level_desc = tk.Label(self, text=game_save.top_level().desc, fg='white', bg='black', 
				font=FONT_BUTTON)
				self.label_level_desc.grid(row=4, column=1)
			if game_save.top_level().length:
				self.label_length = tk.Label(self, text='Length', fg='white', bg='black', 
					font=FONT_TITLE_DESC)
				self.label_length.grid(row=5, column=1)
				self.label_level_length = tk.Label(self, text=game_save.top_level().length, fg='white', bg='black', 
				font=FONT_BUTTON)
				self.label_level_length.grid(row=6, column=1)

			self.button_scan_select = tk.Button(self, text='Select', font=FONT_BUTTON, 
				command=lambda: self.prepare(game_save, [self.label_name,
					self.label_level_name,
					self.label_desc,
					self.label_level_desc,
					self.label_length,
					self.label_level_length,
					self.button_scan_select,
					self.button_scan_cancel]))
			self.button_scan_select.grid(row=7, column=0)
			self.button_scan_cancel = tk.Button(self, text='Rescan', font=FONT_BUTTON,
				command=lambda: self.scan([self.label_name,
					self.label_level_name,
					self.label_desc,
					self.label_level_desc,
					self.label_length,
					self.label_level_length,
					self.button_scan_select,
					self.button_scan_cancel]))
			self.button_scan_cancel.grid(row=7, column=2)
		else:
			tk.Label(self, text='Error loading levels, try again.', fg='white', bg='black',
				font=FONT_BUTTON).grid(row=2, column=0, pady=100)

	def cb_cmd_pass(self, var, entry):
		if var.get() == 1:
			entry.grid(row=3, column=1)
		elif var.get() == 0:
			entry.grid_forget()

	def prepare(self, game_save, b_list):
		self.clear_wid(b_list)
		self.label_ready = tk.Label(self, text='Upload ' + game_save.top_level().name + "?", fg='white', bg='black', 
					font=FONT_TITLE_ACTION)
		self.label_ready.grid(row=1, column=1)

		self.pass_entry = tk.Entry(self, fg='white', bg='black', font=FONT_BUTTON)
		self.cb_var = tk.IntVar()
		self.cb_pass = tk.Checkbutton(self, text='Requires Password', variable=self.cb_var, onvalue=1, offvalue=0, 
			command=lambda: self.cb_cmd_pass(self.cb_var, self.pass_entry), fg='white', bg='black', font=FONT_BUTTON)
		self.cb_pass.grid(row=2, column=1)

		self.button_upload = tk.Button(self, text='Upload', font=FONT_BUTTON,
			command=lambda: self.upload(game_save, self.pass_entry.get(), [self.label_ready,
				self.pass_entry,
				self.cb_pass,
				self.button_upload]))
		self.button_upload.grid(row=4, column=1)

	def upload(self, game_save, password, b_list):
		self.clear_wid(b_list)
		level = game_save.top_level().to_gdl()
		if password:
			level.set_pw(password)
		"""self.label_uploading = tk.Label(self, text='Uploading...', fg='white', bg='black',
										font=FONT_BUTTON)
								self.label_uploading.grid(row=2, column=1, pady=100)"""
		if cts.debug():
			level_upload = cts.local_add(level)
			#self.clear_wid(self.label_uploading)
			if level_upload != 0:
				tk.Label(self, text='Level Uploaded!', fg='white', bg='black',
					font=FONT_TITLE_ACTION).grid(row=1, column=1)
				tk.Label(self, text='Name', fg='white', bg='black',
					font=FONT_TITLE_DESC).grid(row=2, column=1)
				tk.Label(self, text=level.name, fg='white', bg='black',
					font=FONT_BUTTON).grid(row=3, column=1)
				tk.Label(self, text='ID', fg='white', bg='black',
					font=FONT_TITLE_DESC).grid(row=4, column=1)
				self.text_upload = tk.Entry(self, state='readonly', readonlybackground='black', fg='white', 
						font=FONT_TITLE_SECOND)
				self.upload_var = tk.StringVar()
				self.upload_var.set(str(level_upload))
				self.text_upload.config(textvariable=self.upload_var)
				self.text_upload.grid(row=5, column=1)
				if password:
					tk.Label(self, text='Password', fg='white', bg='black',
						font=FONT_TITLE_DESC).grid(row=6, column=1)
					self.text_pass = tk.Entry(self, state='readonly', readonlybackground='black', fg='white', 
						font=FONT_TITLE_SECOND)
					self.pass_var = tk.StringVar()
					self.pass_var.set(password)
					self.text_pass.config(textvariable=self.pass_var)
					self.text_pass.grid(row=7, column=1)
			elif level_upload == 0:
				tk.Label(self, text='Upload failed!', fg='white', bg='black',
					font=FONT_TITLE_ACTION).grid(row=2, column=1, pady=100)


class PageDownload(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.winfo_toplevel().geometry('500x330')
		tk.Frame.configure(self, bg='black')
		self.winfo_toplevel().configure(bg='black')
		self.winfo_toplevel().title('Download a Level')
		gui.sound(MUSIC_FALLING)
		tk.Label(self, text='Download Level', fg='white', bg='black', 
			font=FONT_TITLE_SECOND).grid(row=0, column=1, padx=50)
		tk.Button(self, text='Back', font=FONT_BUTTON_SMALL, 
			command=lambda: master.switch_frame(PageTitle)).grid(row=0, column=2)

		self.label_search = tk.Label(self, text="Enter Upload ID", fg='white', bg='black', 
					font=FONT_BUTTON)
		self.label_search.grid(row=1, column=1)
		self.entry_find = tk.Entry(self, fg='white', bg='black', font=FONT_BUTTON)
		self.entry_find.grid(row=2, column=1)
		self.label_pass = tk.Label(self, text="Password", fg='white', bg='black', 
					font=FONT_BUTTON)
		self.label_pass.grid(row=3, column=1)
		self.entry_pass = tk.Entry(self, fg='white', bg='black', font=FONT_BUTTON)
		self.entry_pass.grid(row=4, column=1)
		self.button_search = tk.Button(self, text='Select', font=FONT_BUTTON, 
			command=lambda: self.search(self.entry_find.get(), self.entry_pass.get(), [self.label_search,
				self.entry_find,
				self.label_pass,
				self.entry_pass,
				self.button_search]))
		self.button_search.grid(row=5, column=1)

	def clear_wid(self, obj):
		if isinstance(obj, list):
			for b in obj:
				try:
					b.grid_forget()
				except:
					pass
		else:
			obj.grid_forget()

	def search(self, sid, spw, b_list):
		e_pw = spw
		if not e_pw:
			e_pw = None
		self.clear_wid(b_list)
		self.label_results = tk.Label(self, text="Results", fg='white', bg='black', 
					font=FONT_BUTTON)
		self.label_results.grid(row=1, column=1)
		result_level = cts.get_level_list().get(sid, e_pw)
		if result_level:
			self.label_name = tk.Label(self, text='Name', fg='white', bg='black', 
				font=FONT_TITLE_DESC)
			self.label_name.grid(row=2, column=1)
			self.label_level_name = tk.Label(self, text=result_level.name, fg='white', bg='black', 
			font=FONT_BUTTON)
			self.label_level_name.grid(row=3, column=1)
			self.label_desc = None
			self.label_level_desc = None
			self.label_length = None
			self.label_level_length = None
			if result_level.desc:
				self.label_desc = tk.Label(self, text='Description', fg='white', bg='black', 
					font=FONT_TITLE_DESC)
				self.label_desc.grid(row=4, column=1)
				self.label_level_desc = tk.Label(self, text=result_level.desc, fg='white', bg='black', 
				font=FONT_BUTTON)
				self.label_level_desc.grid(row=5, column=1)
			if result_level.length:
				self.label_length = tk.Label(self, text='Length', fg='white', bg='black', 
					font=FONT_TITLE_DESC)
				self.label_length.grid(row=6, column=1)
				self.label_level_length = tk.Label(self, text=result_level.length, fg='white', bg='black', 
				font=FONT_BUTTON)
				self.label_level_length.grid(row=7, column=1)
			self.button_search = tk.Button(self, text='Select', font=FONT_BUTTON, 
				command=lambda: self.confirm_load(result_level, [self.label_results,
					self.label_name,
					self.label_level_name,
					self.label_desc,
					self.label_level_desc,
					self.label_length,
					self.label_level_length,
					self.button_search]))
			self.button_search.grid(row=8, column=1)

	def confirm_load(self, level, b_list):
		self.clear_wid(b_list)
		self.label_load = tk.Label(self, text="Load " + level.name + "?", fg='white', bg='black', 
					font=FONT_TITLE_ACTION)
		self.label_load.grid(row=1, column=1)
		self.label_warn1 = tk.Label(self, text="WARNING! This will overwrite your Topmost", 
			fg='white', bg='black', font=FONT_BUTTON)
		self.label_warn1.grid(row=2, column=1)
		self.label_warn2 = tk.Label(self, text="level. Only proceed if it\'s a blank level!", 
			fg='white', bg='black', font=FONT_BUTTON)
		self.label_warn2.grid(row=3, column=1)
		self.button_load = tk.Button(self, text='Load Level', font=FONT_BUTTON, 
				command=lambda: self.load(level, [self.label_load,
					self.label_warn1,
					self.label_warn2,
					self.button_load]))
		self.button_load.grid(row=4, column=1)

	def load(self, level, b_list):
		self.clear_wid(b_list)
		game_save = glc.GameSave()
		load_res = game_save.load(str.encode(level.data[2:len(level.data) - 1]))
		if load_res:
			tk.Label(self, text="Level Loaded!", 
				fg='white', bg='black', font=FONT_TITLE_ACTION).grid(row=2, column=1, pady=100)
		else:
			tk.Label(self, text="Hey, you still have Geometry Dash running!", 
				fg='white', bg='black', font=FONT_BUTTON).grid(row=2, column=1, pady=100)