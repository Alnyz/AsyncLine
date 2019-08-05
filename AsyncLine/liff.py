import json, requests
import urllib.parse
from .proto import LegyProtocolFactory
from . import config
from .lib.Gen.liff import FLiffServiceClient as LiffClient
from .lib.Gen.liff.ttypes import *
from .http_client import HttpClient
from frugal.provider import FServiceProvider
from frugal.context import FContext
from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
class Connection(object):
	def __init__(self):
		self.context = FContext()
		self.transport = HttpClient(config.BASE_URL + "/LIFF1")
		self.protocol_factory = TCompactProtocolAcceleratedFactory()
		self.wrapper_factory  = LegyProtocolFactory(self.protocol_factory)
		self.service_provider = FServiceProvider(self.transport, self.wrapper_factory)
		self.client = self.LiffClients()
		
	def call(self, rfunc: str, *args, **kws) -> callable:
		assert isinstance(rfunc, str), 'Function name must be str not '+type(rfunc).__name__
		rfr = getattr(self.client, rfunc, None)
		if rfr:
			return rfr(self.context, *args, **kws)
		else:
			raise Exception(rfunc + ' is not exist')
	
	def LiffClients(self):
		return LiffClient(self.service_provider)
	
	def updateHeaders(self, dict_key_val):
		self.transport._headers.update(dict_key_val)
		
class Liff(Connection):
	def __init__(self, auth):
		super().__init__()
		self.auth = auth
		self.updateHeaders({
			'user-agent': self.auth.UA,
			'x-line-application': self.auth.LA,
		})
		
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try:
				setattr(self, k, v)
			except:
				pass
		self.updateHeaders({
			"X-Line-Access": self.authToken
		})
		
	def allowLiff(self):
		#This method for automitacally allow Liff App
		#Credit: @Ryn
		url = 'https://access.line.me/dialog/api/permissions'
		data = {
			'on': ['P','CM'],
			'off': []
		}	
		headers = {
			'X-Line-Access': self.authToken.strip(),
			'X-Line-Application': self.auth.LA,
			'X-Line-ChannelId': '1603968955',
			'Content-Type': 'application/json'
		}
		requests.post(url, json=data, headers=headers)
		
	async def issueLiffView(self, to: str):
		self.allowLiff()
		context = LiffChatContext(to)
		chat_ctx = LiffContext(chat=context)
		request = LiffViewRequest("1603968955-ORWb9RdY", chat_ctx)
		return await self.call("issueLiffView", request)
	
	
	async def sendFlex(self, to=None, data=None, altText=None):
		"""
		Use this method to send Flex or template message
		
		Args:
			to: string from chat id
			data: HTML data for liff send to chat
			altText: (str, optional) string will display on chat
		
		Return:
			<requests.Response> or True if Response <= 200
		"""
		token   = await self.issueLiffView(to)
		url_    = "line://app/1603968955-ORWb9RdY/?type=text&text={}".format(urllib.parse.quote('Saya Gans'))
		url     = 'https://api.line.me/message/v3/share'
		headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s' % token.accessToken}
		altText = altText if altText else '%s sent a messages' % self.profile.displayName
		data    = data if data else {"type": "bubble","body": {"type": "box","layout": "vertical","contents": [{"type": "text","align": "center","color": "#00FFF3","text": "Yeay my first liff!","wrap": True,"action": {"type": "uri","uri": url}}]}}
		data    = {'messages': [{'type': 'flex','altText': altText,'contents': data}]}
		res     = requests.post(url, headers=headers, data=json.dumps(data))
		return res