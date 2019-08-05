from typing import Union
from .connections import Connection
from .lib.Gen import *
	
class Channel(Connection):
	def __init__(self, auth):
		super().__init__("/CH4")
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
	
	async def approveChannelAndIssueChannelToken(self, channel_id: str) -> ChannelToken:
		return await self.call("approveChannelAndIssueChannelToken", channel_id)

	async def issueChannelToken(self, channel_id: str) -> ChannelToken:
		return await self.call("issueChannelToken", channel_id)

	async def getChannelInfo(self, channel_id: str, locale: str = "EN") -> ChannelInfo:
		return await self.call("getChannelInfo", channel_id, locale)

	async def revokeChannel(self, channel_id: str) -> None:
		return await self.call("revokeChannel", channel_id)

	async def getChannelNotificationSettings(self, locale: str = "EN") -> list:
		return await self.call("getChannelNotificationSettings", locale)

	async def getDomains(self, lastSynced: int) -> list:
		return await self.call("getDomains", lastSynced)

	async def fetchNotificationItems(self, localRev: int) -> NotificationFetchResult:
		return await self.call("fetchNotificationItems", localRev)