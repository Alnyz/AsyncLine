# -*- coding: utf-8 -*-
import os, sys
import hmac
import time, base64
import asyncio
import hashlib
import rsa
import requests
from . import config
from . import models
from .models import SyncAsync
from .connections import Connection
from .lib.Gen.ttypes import *

class Auth(Connection):
	def __init__(self, client_name):
		super().__init__(config.MAIN_PATH)
		self.LA, self.UA = models.ApplicationHeader(client_name).get()
		self.updateHeaders({
			'User-Agent': self.UA,
			'X-Line-Application': self.LA,
			'X-Line-Carrier': config.CARRIER
		})
		self.afterLoginRemote = []

	def remote(self, func):
		self.afterLoginRemote.append(func)

	#crypto
	def __write_val(self, data):
		return (chr(len(data)) + data)
		
	def __gen_message(self, tuple_msg):
		return (''.join(tuple_msg)).encode('utf-8')
		
	def __rsa_crypt(self, message,RSA):
		pub_key = rsa.PublicKey(int(RSA.nvalue, 16), int(RSA.evalue, 16))
		crypto  = rsa.encrypt(message, pub_key)
		return crypto
		
	def _encryptedEmailAndPassword(self, mail, passwd, RSA):
		message_ = (
			self.__write_val(RSA.sessionKey),
			self.__write_val(mail),
			self.__write_val(passwd),
		)
		message = self.__gen_message(message_)
		crypto  = self.__rsa_crypt(message, RSA).hex()
		return crypto
		
	def _encryptedPassword(self, phone, password, RSA):
		message_ = (
			self.__write_val(RSA.sessionKey),
			self.__write_val(phone),
			self.__write_val(passwd),
		)
		message = self.__gen_message(message_)
		crypto  = self.__rsa_crypt(message, RSA).hex()
		return crypto

	def requestEmailConfirmation(self, email, password, ignoreDuplication=False, useEmailOnly=False):
		raise NotImplementedError("for some reasons we removed it.")
		
	def resendEmailConfirmation(self, verifier):
		raise NotImplementedError("for some reasons we removed it.")
		
	def confirmEmail(self, verifier, pincode):
		raise NotImplementedError("for some reasons we removed it.")
		
	def deviceInfo(self, appType=32):
		raise NotImplementedError("for some reasons we removed it.")
		
	def startVerification(self, phoneNumber, region, seed='', appType=32):
		raise NotImplementedError("for some reasons we removed it.")
		
	def changeVerificationMethod(self, sessionId, method):
		raise NotImplementedError("for some reasons we removed it.")
		
	def verifyPhoneNumber(self, sessionId, pincode, seed=''):
		raise NotImplementedError("for some reasons we removed it.")
		
	def registerWithPhoneNumber(self, tuple_verifyPhoneNumber):
		raise NotImplementedError("for some reasons we removed it.")
		
	def registerWithFacebook(self, FBToken, seed='', appType=32, country="JP"):
		raise NotImplementedError("for some reasons we removed it.")
		
	def generateAccessToken(self, authKey, currentMillis=None):
		raise NotImplementedError("for some reasons we removed it.")
		
	def createAccountMigrationPincodeSession(self):
		raise NotImplementedError("for some reasons we removed it.")
		
	def findSnsIdUserStatus(self, snsIdType, snsAccessToken, udidHash, migrationPincodeSessionId, oldUdidHash):
		raise NotImplementedError("for some reasons we removed it.")
		
	def registerWithSnsId(self, snsIdType, snsAccessToken, region, udidHash, deviceInfo, mid, migrationPincodeSessionId):
		raise NotImplementedError("for some reasons we removed it.")

	def waitForPhoneConfirm(self, verifier):
		r = requests.get(config.BASE_URL + config.WAIT_FOR_MOBILE_PATH, headers={
			'X-Line-Access': verifier
		})
		return r

	async def loginWithQrcode(self, longAlive=True, callback=lambda x: print(x), debug=False):
		self.url(config.MAIN_PATH)
		qr = await self.call('getAuthQrcode', True, config.LOGIN_DEVICE_NAME, "")
		if debug:
			print('QR wait for: ', qr.verifier)
		callback("line://au/q/"+qr.verifier)
		r = self.waitForPhoneConfirm(qr.verifier)
		vr = r.json()['result']['verifier']
		if debug:
			print('QR Ready:', vr)
			input('Press enter to continue...')
		self.url(config.AUTH_PATH)
		rq = LoginRequest(
			LoginType.QRCODE,
			IdentityProvider.LINE,
			None,
			None,
			True,
			config.LOGIN_LOCATION,
			config.LOGIN_DEVICE_NAME,
			None,
			vr,
			None,
			2
		)
		lr = await self.call('loginZ', rq)
		if debug:
			print(lr)
		self.updateHeaders({
			'x-line-access': lr.authToken
		})
		self.authToken = lr.authToken
		self.cert = lr.certificate
		await self.afterLogin()


	async def loginWithCredential(self, mail, password, cert=None, callback=lambda x: print(x)):
		self.url(config.MAIN_PATH)
		rsakey = await self.call('getRSAKeyInfo', config.LOGIN_PROVIDER)
		crypt  = self._encryptedEmailAndPassword(mail, password, rsakey)

		self.url(config.AUTH_PATH)
		rq = LoginRequest(
			LoginType.ID_CREDENTIAL,
			IdentityProvider.LINE_PHONE,
			rsakey.keynm,
			crypt,
			True,
			config.LOGIN_LOCATION,
			config.LOGIN_DEVICE_NAME,
			cert,
			None,
			crypt.encode() if type(crypt) == str else crypt, #none, #crypt
			2
		)
		result = await self.call('loginZ', rq)
		self.url(config.MAIN_PATH)
		if result.type == 3:
			callback("%s %s"% (result.verifier,result.pinCode) )
			r = self.waitForPhoneConfirm( result.verifier )
			rq = LoginRequest(
				LoginType.QRCODE,
				IdentityProvider.LINE,
				None, None, True,
				config.LOGIN_LOCATION,
				config.LOGIN_DEVICE_NAME,
				cert, r.json()['result']['verifier'],
				None, 
				2
			)
			self.url(config.AUTH_PATH)
			result = await self.call('loginZ', rq) 
			self.updateHeaders({
				'x-line-access': result.authToken,
			})
			self.authToken = result.authToken
			self.cert = result.certificate
			self.url(config.MAIN_PATH)
		elif result.type == 1:
			self.authToken = result.authToken
			self.cert = result.certificate
			self.updateHeaders({
				'x-line-access': result.authToken
			})
		else:
			raise Exception('Login failed. got result type `%s`' % (result.type) )

		await self.afterLogin()

	async def loginWithAuthToken(self, authToken):
		self.url(config.MAIN_PATH)
		self.updateHeaders({
			'x-line-access': authToken
		})
		self.authToken = authToken
		await self.afterLogin()

	async def afterLogin(self):
		self.url(config.NORMAL_PATH)
		self.profile = await self.call('getProfile')
		self.last_rev = await self.call('getLastOpRevision')
		self.settings = await self.call('getSettings')
		self.authToken = self.authToken
		
		for remoteFunc in self.afterLoginRemote:
			remoteFunc(**{
				'profile': self.profile,
				'settings': self.settings,
				'rev': self.last_rev,
				'mid': self.profile.mid,
				'authToken': self.authToken,
				'cert': getattr(self, 'cert', None),
				'app_header': (self.LA, self.UA)
			})
	
	async def logout(self):
		await self.call("logoutZ")