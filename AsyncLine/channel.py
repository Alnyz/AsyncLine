from typing import Union
from .lib.Gen import *

class Channel(object):
	def __init__(self, auth):
		self.auth = auth
	
	def afterLogin(self, *args, **kwgs):
		self.auth.url("/CH4")
		if args:
			setattr(*args)
		try:
			for k, v in kwgs.items():
				setattr(self, k, v)
		except:
			pass
	
	async def approveChannelAndIssueChannelToken(self, channel_id: str) -> ChannelToken:
		return await self.auth.call("approveChannelAndIssueChannelToken", channel_id)
		
	async def issueChannelToken(self, channel_id: str) -> ChannelToken:
		return await self.auth.call("issueChannelToken", channel_id)
	
	async def getChannelInfo(self, channel_id: str, locale: str = "EN") -> ChannelInfo:
		return await self.auth.call("getChannelInfo", channel_id, locale)
	
	async def revokeChannel(self, channel_id: str) -> None:
		return await self.auth.call("revokeChannel", channel_id)
	
	async def getChannelNotificationSettings(self, locale: str = "EN") -> list:
		return await self.auth.call("getChannelNotificationSettings", locale)
	
	async def getDomains(self, lastSynced: int) -> list:
		return await self.auth.call("getDomains", lastSynced)
	
	async def fetchNotificationItems(self, localRev: int) -> NotificationFetchResult:
		return await self.auth.call("fetchNotificationItems", localRev)