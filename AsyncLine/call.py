from .lib.Gen.ttypes import *
from .connections import Connection

class Call(Connection):
	def __init__(self, auth):
		super().__init__("/V4")
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
	
	async def acquireGroupCallRoute(self, groupId, mediaType=1):
		return await self.call("acquireGroupCallRoute", groupId, mediaType)
	
	async def getUserStatus(self, user_id):
		return await self.call("getUserStatus", user_id)
		
	async def getGroupCall(self, groupId):
		return await self.call("getGroupCall", groupId)
	
	async def inviteIntoGroupCall(self, chatId, contactIds=None, mediaType=1):
		return await self.call("inviteIntoGroupCall", chatId, contactIds, mediaType)