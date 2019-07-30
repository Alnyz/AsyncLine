# -*- coding: utf-8 -*-.
from .auth import Auth
from . import config as Config
from .lib.Gen.ttypes import *
from typing import Union, Any

import asyncio

class Talk(object):
	def __init__(self, client, auth):
		self.auth = auth
		self.client = client
			
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try: setattr(self, k, v)
			except: pass
			
	async def acquireEncryptedAccessToken(self, featureType: int = 2) -> str:
		"""
		Use this method for get your Encryption Token.
		Args:
			featureType class :lib.Gen.ttypes.FeatureType:
				1 = OBS_VIDEO
				2 = OBS_GENERAL
		
		Return:
			class :str:
		"""
		return await self.auth.call("acquireEncryptedAccessToken", featureType)
		
	async def getProfile(self) -> Profile:
		"""
		A simple method for get your infomations. Requires no parameters.
		
		Return:
			class <class 'LineSync.lib.Gen.ttypes.Profile'>
		"""
		return await self.auth.call("getProfile")
	
	async def getSettings(self) -> Settings:
		"""
		A simple method for testing your Settings. Requires no parameters.
		
		Return:
			class <class 'LineSync.lib.Gen.ttypes.Settings'>
		"""
		return await self.auth.call("getSettings")
	
	async def getUserTicket(self) -> Union[str, Ticket]:
		"""
		A simple method for create your ticket. Requires no parameters.
		
		Return:
			class <class 'LineSync.lib.Gen.ttypes.Ticket'>
		"""
		return await self.auth.call("getUserTicket")
		
	async def generateUserTicket(self,
										expirationTime: int = 100,
										maxUseCount: int = 100) -> Ticket:
		"""
		Use this method for genereate your Ticket.
		
		Args:
			expirationTime: number for your Ticket until this expiration
			maxUseCount: number for set max user can used your Ticket
		Return:
			class <class 'LineSync.lib.Gen.ttypes.Ticket'>
		"""
		try:
			return await self.getUserTicket()
		except:
			await self.reissueUserTicket(expirationTime,  maxUseCount)
			return await self.getUserTicket()
	
	async def reissueGroupTicket(self, group_id: str) -> str:
		"""
		Use this method for getting group Ticket.
		
		Args:
			group_id: string of group_id
			
		Return:
			class :str:
		"""
		return await self.auth.call("reissueGroupTicket", group_id)
		
	async def reissueUserTicket(self, expirationTime: int = 100, maxUseCount: int = 10) -> str:
		"""
		Use this method for genereate your Ticket.
		
		Args:
			expirationTime: number for your Ticket until this expiration
			maxUseCount: number for set max user can used your Ticket
		Return:
			class :str:
		"""
		return await self.auth.call("reissueUserTicket", expirationTime, maxUseCount)

	async def updateProfile(self, profile_obj: Profile) -> bool:
		"""
		Use this method for change your Profile Attribute.
		
		Args:
			profile_obj: profile obj from <class 'LineSync.lib.Gen.ttypes.Profile'>
			
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("updateProfile", 0, profile_obj))
	
	async def updateSettings(self, settings_obj: Settings) -> bool:
		"""
		Use this method for change your Settings Attribute.
		
		Args:
			profile_obj: profile obj from <class 'LineSync.lib.Gen.ttypes.Settings'>
			
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("updateSettings", 0, settings_obj))
		
	async def updateProfileAttribute(self, attribute: ProfileAttribute, value: str) -> bool:
		"""
		Use this method for change your ProfileAttribute.
		
		Args:
			attribute: int of ProfileAttribute <class 'LineSync.lib.Gen.ttypes.ProfileAttribute>
					ALL = 511
					EMAIL = 1
					DISPLAY_NAME = 2
					PHONETIC_NAME = 4
					PICTURE = 8
					STATUS_MESSAGE = 16
					ALLOW_SEARCH_BY_USERID = 32
					ALLOW_SEARCH_BY_EMAIL = 64
					BUDDY_STATUS = 128
					MUSIC_PROFILE = 256
			value: value for attribute will passed as string
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		
		return bool(await self.auth.call("updateProfileAttribute", 0, attribute, value))
		
	async def updateContactSetting(self, mid: str, attribute: int, value: str):
		"""
		Use this method to Update your ContactSettings.
		
		Args:
			attribute: int of ContactSettings <class 'LineSync.lib.Gen.ttypes.ProfileAttribute>
					CONTACT_SETTING_NOTIFICATION_DISABLE = 1
					CONTACT_SETTING_DISPLAY_NAME_OVERRIDE = 2
					CONTACT_SETTING_CONTACT_HIDE = 4.
					CONTACT_SETTING_FAVORITE = 8
					CONTACT_SETTING_DELETE = 16
			value: value for attribute will passed as string
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("updateContactSetting", 0, mid, attribute, value))
	
	async def disableNotifContact(self, mid, str):
		"""
		A simple method for disable notification message from your contact.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 1, "True"))
	
	async def renameContact(self, mid: str, new_name: str):
		"""
		A simple method for disable rename your contact.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 2, new_name))
		
	async def addContactToHiddenList(self, mid: str):
		"""
		A simple method for add your contact into hidden list.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 4, "True"))
	
	async def addContactToFavouriteList(self, mid: str):
		"""
		A simple method for add your contact into favorite list.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 8, "True"))
		
	async def deleteContact(self, mid):
		"""
		A simple method for deleted your friend contact.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 16, "True"))
	
	async def removeContactFromHiddenList(self, mid: str):
		"""
		A simple method for remve your contact into hidden list.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 4, "False"))
	
	async def removeContactFromFavouriteList(self, mid: str):
		"""
		A simple method for remve your contact into hidden favorite list.
		
		Args:
			mid: string of user mid
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		return bool(await self.updateContactSetting(mid, 8, "False"))
	
	async def getContacts(self, mids: Union[str, list, tuple]) -> Union[Contact, list]:
		"""
		Use this method to get information from specifiec mid
		
		Args:
			mids: pass string or multiple mids as list of strings for getting
               more than one Contact at once.
		
		Return:
			<class 'LineSync.lib.Gen.ttypes.Contact>
			or
			<class 'list'>
		"""
		mids = mids if isinstance(mids, (list, tuple)) else [mids]
		if len(mids) <= 1:
			return await self.auth.call("getContact", mids[0])
		else:
			return await self.auth.call("getContacts", mids)
	
	async def blockContact(self, mids: Union[str, list, tuple]) -> bool:
		"""
		Use this method to block contacts from specifiec mid
		
		Args:
			mids: pass string or multiple mids as list of strings for blocking
               more than one Contact at once.
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		if isinstance(mids, str):
			return bool(await self.auth.call("blockContact", 0, mids))
		elif isinstance(mids, (list, tuple)):
			for mid in mids:
				bool(await self.auth.call("blockContact", 0, mid))
	
	async def unblockContact(self, mids: Union[str, list, tuple]) -> bool:
		"""
		Use this method to unblock contacts from specifiec mid
		
		Args:
			mids: pass string or multiple mids as list of strings for unblocking
               more than one Contact at once.
		
		Return:
			bool == false, because this will returning NoneType as False
		"""
		if isinstance(mids, str):	
			return bool(await self.auth.call("unblockContact",0, mids, ""))
		elif isinstance(mids, (list, tuple)):
				for mid in mids:
					bool(await self.auth.call("unblockContact",0, mid, ""))
	
	async def findAndAddContactsByMid(self, mids: str) -> bool:
		"""
		Use this method to find and add contact by mid
		
		Args:
			mids: string of mids users
            
           Return:
           	bool == false, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("findAndAddContactsByMid", 0, mids, 0, ""))
	
	async def findAndAddContactsByUserid(self, user_id: str) -> bool:
		"""
		Use this method to find and add contact by user_id
		
		Args:
			user_id: pass string from user id
            
           Return:
           	bool == false, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("findAndAddContactsByUserid", 0, user_id))
		
	async def findContactByUserid(self, user_id: str) -> Contact:
		"""
		Use this method to find contact by user_id
		
		Args:
			user_id: pass string of user id
            
           Return:
           	<class 'LineSync.lib.Gen.ttypes.Contact'>
		"""
		return await self.auth.call("findContactByUserid", user_id)
		
				
	async def findContactByTicket(self, ticket: str) -> Contact:
		"""
		Use this method to find contact by ticket user
		
		Args:
			ticket: pass string of user id
            
           Return:
           	<class 'LineSync.lib.Gen.ttypes.Contact'>
		"""
		return await self.auth.call("findContactByUserTicket", ticket)
	
	async def getAllContactIds(self) -> list:
		"""
		A simple method to get all of mid from your contacts
		
           Return:
           	<class 'list'>
		"""
		return await self.auth.call("getAllContactIds")
	
	async def getBlockedContactIds(self) -> list:
		"""
		A simple method to get all of mid from your blocked contacts
		
           Return:
           	<class 'list'>
		"""
		return await self.auth.call("getBlockedContactIds")
	
	async def getFavoriteMids(self) -> list:
		"""
		A simple method to get all of mid from your favorite contacts
		
           Return:
           	<class 'list'>
		"""
		return await self.auth.call("getFavoriteMids")
		
	async def getHiddenContactMids(self) -> list:
		"""
		A simple method to get all of mid from your hidden contacts
		
           Return:
           	<class 'list'>
		"""
		return await self.auth.call("getHiddenContactMids")
	
	async def createGroup(self, name: str, mid_users: list) -> bool:
		"""
		Use this method to create group and invite all user using mids
		
		Args:
			name: string of name group for group creating
			mid_users: list of mids user want to invite
			
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("createGroup", 0, name, mid_users))
		
	async def getGroups(self, group_ids: Union[str, list]) -> Union[list, Group]:
		"""
		Use this method to get Informations about group
		
		Args:
			group_ids: string or multiple group_ids of list
							for getting more than once
		
		Return:
			<class 'LineSync.lib.Gen.ttypes.Group'> if group_ids only one
			if list returned <class 'list'>
		"""
		ids = group_ids if isinstance(group_ids, list) else [group_ids]
		if len(ids) <= 1:
			return await self.auth.call("getGroup", ids[0])
		else:
			return await self.auth.call("getGroups", ids)
			
	async def getGroupWithoutMembers(self, group_id: str) -> Group:
		"""
		Use this method to get Informations about group exclude Contact classes
		
		Args:
			group_id: string of group_id
			
		Return:
			<class 'LineSync.lib.Gen.ttypes.Group'>
		"""
		return await self.auth.call("getGroupWithoutMembers", group_id)
		
	async def getGroupsV2(self, group_id: Union[list, str]) -> Group:
		"""
		Use this method to get Custom Informations about group
		include Mid of list members and Mid of list pending members
		more than fasted than getGroups and getCompactGroup
		
		Args:
			group_id: string of group_id
			
		Return:
			<class 'LineSync.lib.Gen.ttypes.Group'>
			or <class 'list'>
		"""
		return await self.auth.call("getGroupsV2", group_id)
		
	async def getCompactGroup(self, group_id: str) -> Group:
		"""
		Use this method to get Compact Informations about group
		exclude some data and fasted than getGroups
		
		Args:
			group_id: string of group id
			
		Return:
			<class 'LineSync.lib.Gen.ttypes.Group'>
		"""
		return await self.auth.call("getCompactGroup", group_id)
	
	async def getGroupIdsInvited(self) -> list:
		"""
		Use this method to get all id of you have invited
		
		Return:
			<class 'list'>
		"""
		return await self.auth.call("getGroupIdsInvited")
	
	async def getGroupIdsJoined(self) -> list:
		"""
		Use this method to get all id of you have joined
		
		Return:
			<class 'list'>
		"""
		return await self.auth.call("getGroupIdsJoined")
	
	async def acceptGroupInvitation(self, group_id: str, ticket: str = None) -> bool:
		"""
		Use this method to join into specifiec group_id, or using ticket id if not None
		
		Args:
			group_id: string of group_id
			ticket: string of ticket from group
		
		Return:
			bool == False, because this will returning NoneType as False
		"""
		if ticket is not None:
			return bool(await self.auth.call("acceptGroupInvitationByTicket", 0, group_id, ticket))
		else:
			return bool(await self.auth.call("acceptGroupInvitation", 0, group_id))
		

	async def cancelGroupInvitation(self, group_id: str, mid_users: Union[str, list]) -> bool:
		"""
		Use this method to cancel invitation user from group
		
		Args:
			group_id: string of id from group id
			mid_users: string or multiple list of string from mid_users
							to cancel more than once
							
		Return:
			bool == False, because this will returning NoneType as False
		"""
		mid_users = mid_users if isinstance(mid_users, list) else [mid_users]
		if len(mid_users) >= 1:
			for mid in mid_users:
				bool(await self.auth.call("cancelGroupInvitation", 0, group_id, [mid]))
		else:
			return bool(await self.auth.call("cancelGroupInvitation", 0, group_id, mid_users))
			
	async def inviteIntoGroup(self, group_id: str, mid_users: list) -> bool:
		"""
		Use this method to invite some or many user into group
		
		Args:
			group_id: string of id from group id
			mid_users: string or multiple list of string from mid_users
							to invite more than once
							
		Return:
			bool == False, because this will returning NoneType as False
		"""
		mids = mid_users if isinstance(mid_users, list) else [mid_users]
		return bool(await self.auth.call("inviteIntoGroup", 0, group_id, mids))
	
	async def kickoutFromGroup(self, group_id: str, mid_users: Union[str, list]) -> bool:
		"""
		Use this method to kick some or many user from group
		
		Args:
			group_id: string of id from group id
			mid_users: string or multiple list of string from mid_users
							to kick more than once
							
		Return:
			bool == False, because this will returning NoneType as False
		"""
		mids = mid_users if isinstance(mid_users, list) else [mid_users]
		if len(mids) > 1:
			for mid in mids:
				bool(await self.auth.call("kickoutFromGroup", 0, group_id, [mid]))
		else:
			return bool(await self.auth.call("kickoutFromGroup", 0, group_id, mids))
			
	async def leaveGroup(self, group_id: str) -> bool:
		"""
		Use this method to leave from group
		
		Args:
			group_id: string of id from group id
			
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("leaveGroup", 0, group_id))
	
	async def rejectGroupInvitation(self, group_id: str) -> None:
		"""
		Use this method to reject group you have invited
		
		Args:
			group_id: string of id from group id, see self.getGroupIdsInvited
			
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("rejectGroupInvitation", 0, group_id))
	
	async def updateGroupPreferenceAttribute(self, group_id:str, attribute: dict) -> bool:
		"""
		Use this method to update yoir Preference attribute of group
		
		Args:
			group_id: string of id from group id
			attribute: dict of attribute from {<class 'LineSync.lib.Gen.ttypes.GroupPreferenceAttribute'>, string}
							INVITATION_TICKET = 1
							FAVORITE_TIMESTAMP = 2
							
							e.g: cl.updateGroupPreferenceAttribute(group_id, {1: "True"})
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("updateGroupPreferenceAttribute", 0, group_id, attribute))
		
	async def updateGroup(self, obj: Union[Group]) -> bool:
		"""
		Use this method to update Group attribute
		
		Args:
			obj: object from Group classes <class 'LineSync.lib.Gen.ttypes.Group'>
			
			e.g:
				group = client.getGroup(group_id)
				group.preventedJoinByTicket = False
				client.updateGroup(group)
				
				this will disable Joining by ticket group
				
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return bool(await self.auth.call("updateGroup", 0, obj))
	
	async def getRoom(self, room_id: str) -> Room:
		"""
		Use this method to get Room Informations
		
		Args:
			room_id: string of room_id
			
		Return:
			<class 'LineSync.lib.Gen.ttypes.Room'>
		"""
		return await self.auth.call("getRoom", room_id)
		
	async def getCompactRoom(self, room_id: str) -> Room:
		"""
		Use this method to get Compact Room Informations
		fasted than getRoom
		
		Args:
			room_id: string of room_id
			
		Return:
			<class 'LineSync.lib.Gen.ttypes.Room'>
		"""
		return await self.auth.call("getCompactRoom", room_id)
	
	async def inviteIntoRoom(self,room_id:str, mid_users: Union[str, list]) -> bool:
		"""
		Use this method to invite some or many user into room
		
		Args:
			room_id: string of id from room id
			mid_users: string or multiple list of string from mid_users
							to invite more than once
							
		Return:
			bool == False, because this will returning NoneType as False
		"""
		mids = mid_users if isinstance(mid_users, list) else [mid_users]
		return await self.auth.call("inviteIntoRoom", 0, room_id, mids)
		
	async def leaveRoom(self, room_id: str) -> bool:
		"""
		Use this method to leave from room
		
		Args:
			room_id: string of id from room id
			
		Return:
			bool == False, because this will returning NoneType as False
		"""
		return await self.auth.call("leaveRoom", 0, room_id)
		
	async def sendMessage(self,
						group_id: str,
						text: str,
						contentMetadata: Union[dict] = None,
						contentType: int = 0
					) -> Union[str, Message]:
		"""
		Use this method to sending Message containt any types
		
		Args:
			group_id: string of mid from group id
			text: string of some text
			contentMetadata: dict of contentMetadata for sending
			contentType: int of contentType see <class 'LineSync.lib.Gen.ttypes.ContentType'>
		
		Return:
			<class 'LineSync.lib.Gen.ttypes.Message'>
		"""	
		msg = Message(to=group_id,
							text = text,
							contentType =  contentType,
							contentMetadata = {'LINE_RECV':'1'} 
							if contentMetadata is None \
							else contentMetadata
						)
		return await self.auth.call("sendMessage", 0, msg)
		
	async def getMidWithTag(self, message: Message) -> list:
		"""
		Use this method to get mid of user using Mention
		
		Args:
			message: <class 'LineSync.lib.Gen.ttypes.Message'>
			
			e.g
			async def _(op):
				message = op.message
				await client.getMidWithTag(message)
				
		Return:
			<class 'list'> of mid user
		"""
		if message.contentMetadata["MENTION"] \
			and message.contentMetadata is not None:
			key = eval(messages.contentMetadata["MENTION"])
			if len(key["MENTIONEES"]) <= 1:
				return list(key["MENTIONEES"][0]["M"])
			else:
				mm = []
				for mid in key["MENTIONEES"]:
					mm.append(mid["M"])
				return mm
	
	async def sendAudio(self,
								to: str,
								path: str = None,
								url: str = None,
								remove_path: bool = False) -> bool:
		"""
		Use this method to send Audio message
		important if args url is given, it cannot use the path
		
		Args:
			to: mid of group or user will be send
			path: string of path where audio will be send
			url: string of url from audio
			remove_path: set a bool parameter for deleting temp file after download contentremove_path: set a bool parameter for deleting temp file after download content
			
		Return:
			<class 'bool'> is True
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use the path")
		if path is None and url is not None:
			path = await self.client.download_fileUrl(url)
			
		objectId = (await self.sendMessage(to, text=None, contentType = 3)).id
		return self.client.uploadObjTalk(path=path, types='audio', remove_path=remove_path, objId=objectId)
		
	async def sendImage(self,
								to: str,
								path: str = None,
								url: str = None,
								remove_path: bool = False) -> bool:
		"""
		Use this method to send Image message
		important if args url is given, it cannot use the path
		
		Args:
			to: mid of group or user will be send
			path: string of path where image will be send
			url: string of url from image
			remove_path: set a bool parameter for deleting temp file after download content
			
		Return:
			<class 'bool'> is True
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use the path")
		if url is not None and path is None:
			path = await self.client.download_fileUrl(url)
				
		objectId = (await self.sendMessage(to, text=None, contentType=1)).id
		return await self.client.uploadObjTalk(path=path, types='image', remove_path=remove_path, objId=objectId)
	
	async def sendVideo(self,
								to: str,
								path: str = None,
								url: str = None,
								remove_path: bool = False) -> bool:
		"""
		Use this method to send Video message
		important if args url is given, it cannot use the path
		
		Args:
			to: mid of group or user will be send
			path: string of path where Video will be send
			url: string of url from video
			remove_path: set a bool parameter for deleting temp file after download content
			
		Return:
			<class 'bool'> is True
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use the path")
		if url is not None and path is None:
			path = await self.client.download_fileUrl(url)
			
		objectId = (await self.sendMessage(to, text=None, contentMetadata={'VIDLEN': '60000','DURATION': '60000'}, contentType = 2)).id
		return await self.client.uploadObjTalk(path=path, types='video', remove_path=remove_path, objId=objectId)
	
	async def sendGif(self,
								to: str,
								path: str = None,
								url: str = None,
								remove_path: bool = False) -> bool:
		"""
		Use this method to send Gif message
		important if args url is given, it cannot use the path
		
		Args:
			to: mid of group or user will be send
			path: string of path where Gif will be send
			url: string of url from Gif
			remove_path: set a bool parameter for deleting temp file after download content
			
		Return:
			<class 'bool'> is True
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use the path")
		if url is not None and path is None:
			path = await self.client.download_fileUrl(url)
			
		return await self.client.uploadObjTalk(to=to, path=path, types='gif', remove_path=remove_path)
	
	async def sendFile(self, to: str, path: str = None, file_name: str = None):
		"""
		Use this method to send File message
		important if args url is given, it cannot use the path
		
		Args:
			to: mid of group or user will be send
			path: string of path where file will be send
			url: string of url from file
		
		Return:
			<class 'bool'> is True
		"""
		fp = open(path, 'rb')
		if file_name is None:
			file_name = fp.name
		objectId = (await self.sendMessage(to, text=None, contentMetadata={'FILE_NAME': str(file_name),'FILE_SIZE': str(len(fp.read()))}, contentType = 14)).id
		return await self.client.uploadObjTalk(path=path, types='file', remove_path=remove_path, objId=objectId)
		
	async def fetchOps(self, localRev, count=10):
		return await self.client.call('fetchOps', localRev, count, 0, 0)
		
	async def fetchOperations(self, localRev, count=10):
		return await self.client.call('fetchOperations', localRev, count)