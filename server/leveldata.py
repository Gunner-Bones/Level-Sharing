import sys
import random
sys.path.insert(0, '..')
from tools.json_abs import *


JSON_LEVELS = 'server/levels'
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
		self.used_ids = []

	def add(self, gd_level):
		add_level = gd_level
		new_id = random.randint(10000, 99999)
		if new_id in self.used_ids:
			while new_id in self.used_ids:
				new_id = random.randint(10000, 99999)
		add_level.set_id(new_id)
		self.levels.append(add_level)
		self.up()
		return new_id

	def delete(self, gd_level):
		rem_id = gd_level.lid
		rem_level = None
		for level in self.levels:
			if level.lid == rem_id:
				rem_level = level
				break
		if rem_level:
			self.levels.remove(level)
			self.used_ids.remove(rem_id)
			self.up()
			return True
		return False

	def get(self, lid, pw=None):
		for level in self.levels:
			if level.lid == int(lid):
				if level.pw:
					if pw:
						if level.pw == pw:
							return level
						return
					return
				else:
					return level

	def clear(self):
		# Debug only
		self.levels = []
		self.used_ids = []
		self.up()
		print('[DEBUG] levels.json cleared')

	def up(self):
		up_list = [level.get_json() for level in self.levels]
		current = j_read(JSON_LEVELS)
		if current != up_list or not current:
			j_overwrite(JSON_LEVELS, up_list)

	def down(self):
		down_list = j_read(JSON_LEVELS)
		if down_list:
			self.levels = [GDLevel(
				name=level["name"],
				desc=level["desc"],
				length=level["length"],
				author=level["author"],
				pw=level["password"],
				lid=level["id"],
				data=level["data"]) for level in down_list]
			self.used_ids = [level['id'] for level in down_list]


class GDLevel:
	def __init__(self, name, data, desc=None, length=None, author=None, pw=None, lid=0):
		self.name = name
		self.desc = desc
		self.length = length
		self.data = data
		self.author = author
		self.pw = pw
		self.lid = lid

	def set_id(self, lid):
		self.lid = lid

	def set_pw(self, pw):
		self.pw = pw

	def get_json(self):
		return {
			"name": self.name,
			"desc": self.desc,
			"length": self.length,
			"data": self.data,
			"author": self.author,
			"password": self.pw,
			"id": self.lid
		}

	def __str__(self):
		return self.get_json()
