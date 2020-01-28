try:
	import tools.gdlevelclient as lc
except ModuleNotFoundError:
	print('[WARNING] Running without tools.gd levelclient')
import tools.gui as gui
import pages
import tkinter as tk


if __name__ == '__main__':
	main = gui.TkView()
	main.mainloop()