# -*- coding: utf-8 -*-
import traceback, asyncio
from . import config
from . import models
from .filters import Filter
from .connections import Connection
from thrift.transport.TTransport import TTransportException
from .lib.Gen.ttypes import *
from inspect import *
from types import LambdaType

class Handler:
	def __init__(self, callback, done=False):
		self.callback = callback
		self.done = done
		
	def __getitem__(self, item):
		return getattr(self, item)
		
class Poll(Connection):
	def __init__(self, client, loop=None):
		super().__init__(config.POLLING_PATH)
		self.transport.setTimeout(-1)
		self._client = client
		self.LA, self.UA = self._client.LA, self._client.UA
		self.updateHeaders({
			'User-Agent': self.UA,
			'X-Line-Application': self.LA,
		})
		self.revision = 0
		self.loop = loop if loop else asyncio.get_event_loop()
		self.transport.loop = self.loop
		self.plug_handler = {}
		self.convers_handler = {}
		self.fetch_event = asyncio.Event(loop=self.loop)
		if self._client.client_name in ['android', 'android2']:
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
			'X-Line-Access': self.authToken
		})

	def streams(self):
		self.loop.run_until_complete(self.run_fetch())
	
	def conversation(self, msg, callback, done=False):
		cid = msg.from_
		msg.callback = callback
		if cid in self.convers_handler.keys():
			self.convers_handler[cid].append(Handler(msg.callback, done))
		else:
			self.convers_handler[cid] = [Handler(msg.callback, done)]
			
	async def fetchOps(self, localRev, count=10):
		return await self.call('fetchOps', localRev, count, 0, 0)
		
	async def fetchOperations(self, localRev, count=10):
		return await self.call('fetchOperations', localRev, count)
	
	async def execute(self, coro, *args, **kwgs):
		if isroutine(coro) or iscoroutinefunction(coro):
			await coro(*args, **kwgs)
		else:
			coro(*args, **kwgs)
		
	async def setRevision(self, revision):
		self.revision = max(revision, self.revision)
	
	async def run_fetch(self, limit=1):
		#TODO: Make it efficient
		while not self.fetch_event.is_set():
			try:
				ops = await self.fetch(self.revision, limit)
				for op in ops:
					self.revision = max(self.revision, op.revision)
					if self.plug_handler:
						for handle, hFuncs in self.plug_handler.items():
							if handle == op.type:
								for hFunc in hFuncs:
									for k, v in hFunc.items():
										if hFunc[k][0] is not None and isinstance(hFunc[k][0], Filter):
											if hFunc[k][0](op.message):
												await self.execute(k, hFunc[k][1], op.message)
										elif isinstance(hFunc[k][0], LambdaType):
											if hFunc[k][0](hFunc[k][1], op if op.type not in [25, 26] else op.message):
												await self.execute(k, hFunc[k][1], 
													op if op.type not in [25,26] \
													else op.message)
										elif hFunc[k][0] is None:
											await self.execute(k, hFunc[k][1], op)
					if self.convers_handler != {} and (op.type == 26 and op.message.toType == 0):
						cid = op.message.from_
						if cid in self.convers_handler.keys():
							handlers = self.convers_handler.get(cid, None)
							if handlers:
								for handler in handlers:
									new_fetch = ops
									default_callback = handler.callback
									for fetch in new_fetch:
										if fetch.message.from_ in self.convers_handler.keys() and not fetch.message.command:
											if not handler.done:
												await self.execute(default_callback, fetch.message)
											else:
												await self.execute(default_callback, fetch.message)
												self.convers_handler.pop(fetch.message.from_)
										else:
											continue
			except EOFError:
				continue
			except TTransportException:
				self.fetch_event.clear()
				break
			except KeyboardInterrupt:
				raise
			except ShouldSyncException:
				self.fetch_event.clear()
				pass
			except Exception:
				print(traceback.format_exc())