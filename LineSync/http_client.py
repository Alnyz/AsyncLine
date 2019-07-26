# -*- coding: utf-8 -*-
import os,sys,time

import async_timeout, asyncio
from aiohttp.client import ClientSession

from thrift.transport.TTransport import TTransportBase
from thrift.transport.TTransport import TMemoryBuffer
from thrift.transport.TTransport import TTransportException

from frugal.aio.transport import FTransportBase
from frugal.context import FContext
from frugal.aio.transport.http_transport import FHttpTransport

from frugal.exceptions import TTransportExceptionType

class HttpClient(FHttpTransport):
	def __init__(self, url, timeout=5000):
		super().__init__(0)
		self._url = url
		self.setTimeout(timeout) 
		self._headers = {
			'content-type': 'application/x-thrift',
			'accept': 'application/x-thrift',
			'user-agent': 'Python Frugal Thrift',
		}
		
	def setTimeout(self, timeout):
		self._timeout = timeout

	async def request(self, context: FContext, payload) -> TTransportBase:
		payload = payload[4:] 
		self._payload = payload
		self._preflight_request_check(payload) 
		status, text = await self._make_request(context, payload)
		if status == 400: 
			raise TTransportException(
				type=400, 
				message='Bad request: '+str(text) + ' :: '+ str(payload))
		elif status == 403:
			raise TTransportException(
				type=403, 
				message='Forbidden: '+str(text))
		elif status == 404:
			raise TTransportException(
				type=404,
				message='Not Found: '+str(text))
		elif status == 410:
			pass
		elif status == 500:
			raise TTransportException(
				type=500,
				message='Backend Error: '+str(text))
		elif status >= 300:
			raise TTransportException(
				type=TTransportExceptionType.UNKNOWN,
				message='request errored with {0} and message {1}'.format(
					status, str(text)
					))

		return TMemoryBuffer(text)
		
	async def _make_request(self, context:FContext, payload):
		async with ClientSession() as session:
			try:
				if self._timeout > 0:
					with async_timeout.timeout(self._timeout / 1000):
						async with session.post(self._url, 
											data=payload,
											headers=self._headers) \
							as response:
							return response.status, await response.content.read()
				else:
					async with session.post(self._url,data=payload,headers=self._headers) as response:
						return response.status, await response.content.read()
			except asyncio.TimeoutError:
				raise TTransportException(
					type=TTransportExceptionType.TIMED_OUT,
					message='request timed out'
					)