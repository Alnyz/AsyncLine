from .connections import Connection
from .lib.Gen.ttypes import *
from typing import Union

class Shop(Connection):
	def __init__(self, auth):
		super().__init__("/SHOP4")
		self.auth = auth
		self.updateHeaders({
			'User-Agent': self.auth.UA,
			'X-Line-Application': self.auth.LA,
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
	
	async def getBalance(self, appStoreCode: int = 1) -> Coin:
		return await self.call("getTotalBalance", appStoreCode)
		
	async def getProduct(self, packageId: int, language: str = "EN", country: str = "ID") -> Product:
		return await self.call("getProduct", packageId, language, country)
	
	async def getProductList(self, productIdList: Union[str, list], language: str = "EN", country: str ="ID") -> ProductList:
		productIdList = productIdList if isinstance(productIdList, list) else [productIdList]
		return await self.call("getProductList", productIdList, language, country)
	
	async def getPurchaseHistory(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getPurchaseHistory", start, size, language, country)
	
	async def getPresentsSent(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getPresentsSent", start, size, language, country)
	
	async def getPresentsReceive(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getPresentsReceived", start, size, language, country)
	
	async def getDownloads(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getDownloads", start, size, language, country)
	
	async def getEventPackages(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getEventPackages", start, size, language, country)
	
	async def getNewlyReleasedPackages(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getNewlyReleasedPackages", start, size, language, country)
		
	async def getPopularPackages(self, start: int = 1, size: int = 10, language: str = "EN", country: str = "ID") -> ProductList:
		return await self.call("getPopularPackages", start, size, language, country)
	
	async def buyFreeProduct(self,
								receiverMid: str,
								productId: str = None,
								packageId: int = None,
								messageTemplate: int = 1,
								language: str = "EN",
								country: str = "ID"):
		return await self.call("buyFreeProduct", receiverMid=receiverMid,
								productId=productId, packageId=packageId,
								messageTemplate=messageTemplate,
								language=language, country=country
							)
							
	async def buyCoinProduct(self,
								receiverMid: str,
								productId: str = None,
								packageId: int = None,
								language: str = "EN",
								location: str = None,
								currency: str = None,
								price: str = None,
								appStoreCode: int = 1, #0 APPLE,1 GOOGLE
								messageText: str = None,
								messageTemplate: int = 1
							):
		payment = PaymentReservation(receiverMid=receiverMid, productId=productId,
									packageId=packageId, language=language, location=location,
									currency=currency, messageText=messageText, price=price,
									messageTemplate=messageTemplate, appStoreCode=appStoreCode)
		return await self.call("buyCoinProduct", payment)
	
	async def reserveCoinPurchase(self,
										productId: int,
										pgCode: int,
										currency: str,
										price: str,
										appStoreCode: int = 1#0 APPLE, 1 GOOGLE
										redirectUrl: str = None,
										country: str = "ID",
										language: str = "EN"):
		req = CoinPurchaseReservation(
							productId=productId, currency=currency
							pgCode=pgCode, price=price
							appStoreCode=appStoreCode, redirectUrl=redirectUrl,
							language=language, country=country	
						)
		return await self.call("reserveCoinPurchase", req)