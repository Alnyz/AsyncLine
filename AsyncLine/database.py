from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Union, List


class Storage(object):
	def __init__(self, host, db_name=None, col_name=None):
		self.client = MongoClient(host, ssl=True, authSource="admin")
		self.db_name = db_name
		self.col_name = col_name
		self.database = self.client[self.db_name]
		self.col = self.database[col_name]
		self.auth_col = self.database['col_auth']
		
	def add_data(self, data: Union[dict, List[dict]], col: Collection = None):
		if isinstance(data, list):
			if col:
				col.insert_many(data)
			else:
				self.col.insert_many(data)
		else:
			if col:
				col.insert_one(data)
			else:
				self.col.insert_one(data)

	def update_data(self, query: dict, data: Union[dict, List[dict]] = None, col: Collection = None):
		assert isinstance(query, dict), 'query must dict Value not %' % type(query).__name__
		assert data is not None, "data cannot None value"
		if isinstance(data, list):
			self.col.update_many(query, data)
		else:
			self.col.update_one(query, data)

	def delete_data(self, filter=None, all=False):
		if all and filter is None:
			self.col.delete_many({})
		else:
			self.col.delete_one(filter)

	def find_data(self, col_name=None, filter={}, all = False):
		col = self.database[col_name] if col_name else self.col
		if not all:
			find = col.find_one(filter)
		else:
			find = col.find(filter)
		return [i for i in find] if all else find
	
	def look_db(self):
		return self.client.list_database_names()
	
	def look_col(self, db_name):
		return self.client[db_name].list_collection_names()
		
	def create_col(self, db_name, name):
		"""
		Create a collection if `name` not in Database return Collection if exists
		"""
		db = self.create_db(db_name)
		return Collection(database=db, name=name)

	def create_db(self, db_name):
		"""
		Create a Database if `db_name` not in cluster return `Database` if exists
		"""
		return Database(client=self.client, name=db_name)