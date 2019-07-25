# -*- coding: utf-8 -*-
from . import config
from . import models
from .auth import Auth
from .connections import Connection
from .lib.Gen.ttypes import ShouldSyncException
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
 
from .filters import Filter
from functools import wraps
import traceback, time, asyncio, logging

NOTIF_TYPE = [10, 11, 12, 13, 15, 17, 18, 19, 22, 32]

log = logging.getLogger(__name__)

class DefaultException(Exception):
	def __init__(self):
		super().__init__(self)
		
class Poll(Connection):
	def __init__(self, client_name):
		super().__init__(config.POLLING_PATH)

		self.transport.setTimeout(-1)

		self.LA, self.UA = models.ApplicationHeader(client_name).get()
		self.updateHeaders({
			'user-agent': self.UA,
			'x-line-application': self.LA,
		})
		self.rev = 0
		self.Opinterrupts: list = []
		self.func_handler : list = []
		self._thread: bool = False
		self._workers: int = 3
		self._debug: bool = False
		if client_name in ['android', 'android2']:
			self.fetch = self.fetchOps
		else:
			self.fetch = self.fetchOperations
	
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try: setattr(self, k, v)
			except: pass
		self.setupConnection()
		
	def setupConnection(self):
		self.updateHeaders({
			'x-line-access': self.authToken
		})
		
	def hooks(self, types, *arg, **kwg):
		def decorator(func):
			@wraps(func)
			def wraper(self, *args, **kwgs):
				return func(*args, **kwgs)
			data = {
				func:arg,
				"data":kwg
			}
			self.func_handler.append(data)
			return wraper, self.Opinterrupts.append({types:func})
		return decorator
	
	def exception_handler(self, loop, contex):
		return log.error(traceback.print_exc())
		
	def start_loop(self, loop):
		asyncio.set_event_loop(loop)
		if self._debug:
			loop.set_debug(True)

		loop.slow_callback_duration = 0
		loop.run_forever()
	
	async def _exec(self, func, ops):
		for i in range(len(self.func_handler)):
			if func in self.func_handler[i]:
				if len(self.func_handler[i][func]) < 1:
					await self.do_job(i, ops)
				else:
					if self.func_handler[i][func][0] != None:
						if self.func_handler[i][func][0](ops.message):	
							await self.do_job(i, ops)
					
	async def do_job(self, c, ops):
		if not self._thread:
			await self.Opinterrupts[c][ops.type](ops)
		else:
			try:
				new_loop = asyncio.new_event_loop()
				new_loop.set_default_executor(ThreadPoolExecutor(self._workers))
				t = Thread(name="WorkerThread :{}:".format(self.__class__.__name__),
					target=self.start_loop,
					args=(new_loop,))
				t.start()	
				future = asyncio.run_coroutine_threadsafe(
						self.Opinterrupts[c][ops.type](ops), new_loop
					)
				future.result()
			except Exception as e:
				future.set_exception(DefaultException)
				print(traceback.format_exc())
			
	async def fetchOps(self, localRev, count=10):
		return await self.call('fetchOps', localRev, count, 0, 0)
		
	async def fetchOperations(self, localRev, count=10):
		return await self.call('fetchOperations', localRev, count)
		
	async def setRevision(self, revision):
		rev = await self.call("getLastOpRevision")
		self.rev = max(rev, revision)
		
	async def trace(self):
		ops = await self.fetch(self.rev)
		for op in ops:
			self.rev = max(self.rev, op.revision)
			if self.func_handler:
				for i in range(len(self.Opinterrupts)):						
					if list(self.Opinterrupts[i].values())[0] in self.func_handler[i]:
						if op.type in self.Opinterrupts[i].keys():				
							await self._exec(self.Opinterrupts[i][op.type], op)
		
	async def streams(self):
		try:
			while True:
				await self.trace()
		except EOFError:
			pass
		except ShouldSyncException:
			pass
