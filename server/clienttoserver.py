import sys
import json
sys.path.insert(0, '..')
from tools.json_abs import *
import server.leveldata as ld

# Run Server storing methods locally if this is on. Used for testing until the server is done/while the server is down.
DEBUG = True


def debug():
	return DEBUG


level_list = None
if DEBUG:
	level_list = ld.LevelList()
	level_list.down()


def get_level_list():
	return level_list


def local_add(gdlevel):
	new_id = 0
	new_id = level_list.add(gdlevel)
	return new_id