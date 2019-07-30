# -*- coding: utf-8 -*-
import os, sys, traceback, asyncio
from . import config
from . import models
from .filters import Filter
from .connections import Connection
from concurrent.futures import ThreadPoolExecutor
from functools import partial

class Poll(Connection):
	def __init__(self, client_name):
		super().__init__(config.POLLING_PATH)

		self.transport.setTimeout(-1)

		self.LA, self.UA = models.ApplicationHeader(client_name).get()
		self.updateHeaders({
			'user-agent': self.UA,
			'x-line-application': self.LA,
		})
		self.revision = 0
		self.op_handler = {}
		self._threaded = True
		
		if client_name in ['android', 'android2']:
			self.fetch = self.fetchOps
		else:
			self.fetch = self.fetchOperations

	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try:
				setattr(self, k, v)
			except:
				pass
		self.revision = self.rev
		self.setupConnection()
		
	def setupConnection(self):
		self.updateHeaders({
			'x-line-access': self.authToken
		})

	def hooks(self, **parent_kw):
		def parent(func):
			def wrapper(*args, **kws):
				return func(*args,**kws)
			self.op_handler.setdefault(parent_kw.get('type',-1), []).append({
				wrapper:parent_kw.get("filters", None)
			})
			return wrapper
		return parent

	async def fetchOps(self, localRev, count=10):
		return await self.call('fetchOps', localRev, count, 0, 0)
		
	async def fetchOperations(self, localRev, count=10):
		return await self.call('fetchOperations', localRev, count)
	
	async def execute(self, coro, *args):
		await coro(*args)
	
	async def setRevision(self, revision):
		self.revision = max(revision, self.revision)
		
	async def streams(self, limit=1):
		while True:
			try:
				ops = await self.fetch(self.revision, limit)
				for op in ops:
					self.revision = max(self.revision, op.revision)
					for handle, hFuncs in self.op_handler.items():
						if handle == op.type:
							for hFunc in hFuncs:
								for k, v in hFunc.items():
									if hFunc[k] is not None and isinstance(hFunc[k], Filter):
										if hFunc[k](op.message):
											await self.execute(k, op.message)
									elif hFunc[k] is None:
										await self.execute(k, op)
						else:
							continue
			except EOFError:
				continue
			except Exception:
				print(traceback.format_exc())