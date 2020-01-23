try:
	import tools.gdlevelclient as lc
except ModuleNotFoundError:
	print('[WARNING] Running without tools.gdlevelclient')
import tools.gui as gui
import pages
import tkinter as tk


main = gui.TkView()
main.mainloop()