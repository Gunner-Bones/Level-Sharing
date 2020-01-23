import sys
sys.path.insert(0, '..')
from tools.json_abs import *


JSON_LEVELS = 'levels'
"""
levels.json:
[
	{
		data...
	},
	{
	
	}, ...
]
"""


class LevelList:
	def __init__(self):
		self.levels = []
		self.latest_id = 0

	def add(self, gd_level):
		add_level = gd_level
		self.latest_id += 1
		add_level.set_id(self.latest_id)
		self.levels.append(add_level)

	def up(self):
		up_list = [level.get_json() for level in self.levels]
		current = j_read(JSON_LEVELS)
		if current != up_list:
			j_overwrite(JSON_LEVELS, up_list)

	def down(self):
		down_list = j_read(JSON_LEVELS)
		self.levels = [GDLevel(
			data=level["data"],
			author=level["author"],
			pw=level["password"],
			lid=level["id"]) for level in down_list]
		highest_id = 0
		for level in self.levels:
			if level.lid >= highest_id:
				highest_id = level.lid
		self.latest_id = highest_id


class GDLevel:
	def __init__(self, data, author, pw=None, lid=0):
		self.data = data
		self.author = author
		self.pw = pw
		self.lid = lid

	def set_id(self, lid):
		self.lid = lid

	def get_json(self):
		return {
			"data": self.data,
			"author": self.author,
			"password": self.pw,
			"id": self.lid
		}
