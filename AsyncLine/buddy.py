from .connections import Connection
from .lib.Gen.ttypes import *
from typing import Union, List
class Buddy(Connection):
	def __init__(self, auth):
		super().__init__("/BUDDY4")
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
	
	async def findBuddyContactsByQuery(self,
								query: str,
								fromIndex: int= 1,
								count: int =10,
								requestSource: Union[BuddySearchRequestSource, int] = 0,
								country: str ="ID",
								language: str ="EN") -> Union[List[BuddySearchResult]]:
		return await self.call("findBuddyContactsByQuery", query=query, \
					fromIndex=fromIndex, count=count,
					requestSource=requestSource, \
					country=country, language=language
					)
	
	async def getBuddyContacts(self,
										language: str ="EN",
										country: str ="ID",
										classification: str = "",
										fromIndex: int = 1,
										count: int = 10):
		return await self.call("getBuddyContacts", language=language, \
						country = country, classification = classification, \
						fromIndex = fromIndex, count = count)
						
	async def getBuddyDetail(self, buddyMid: str) -> BuddyDetail:
		return await self.call("getBuddyDetail", buddyMid)
	
	async def getBuddyOnAir(self, buddyMid: str) -> BuddyOnAir:
		return await self.call("getBuddyOnAir", buddyMid)
	
	async def getCountriesHavingBuddy(self) -> list:
		return await self.call("getCountriesHavingBuddy")
	
	async def getNewlyReleasedBuddyIds(self, country: str = "ID") -> dict:
		return await self.call("getNewlyReleasedBuddyIds", country)
		
	async def getPopularBuddyBanner(self,
												language: str = "EN",
												country: str = "ID",
												applicationType: Union[ApplicationType] = 16,
												resourceSpecification: str = ""
											):
		return await self.call("getPopularBuddyBanner",
								language=language, country=country,
								applicationType=applicationType, resourceSpecification=resourceSpecification
							)
	
	async def getPopularBuddyLists(self,
											language: str = "EN",
											country: str = "ID") -> Union[List[BuddyList]]:
		return await self.call("getPopularBuddyLists", language=language, country=country)
		
	async def getPromotedBuddyContacts(self,
											language: str = "EN",
											country: str = "ID") -> Contact:
		return await self.call("getPromotedBuddyContacts", language=language, country=country)
		