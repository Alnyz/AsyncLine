# -*- coding: utf-8 -*-
from .models import *
from .auth import Auth
from .buddy import Buddy
from .poll import Poll
from .channel import Channel
from .talk import Talk
from .call import Call
from .liff import Liff
from .timeline import Timeline
from .shop import Shop
from . import config
from . import log
from .lib.Gen.ttypes import *
from random import randint
from urllib3.response import HTTPResponse
import urllib
import os
import base64
import re
import requests
import time
import json
import tempfile
import shutil
from ffmpy import FFmpeg
logs = log.LOGGER

def callback(*args, **kws):
	print(*args, **kws)
	
class LineNext(object):
	def __init__(self, client_name):
		self.auth = Auth(client_name)
		self.auth.remote(self.afterLogin)
		self.budy = Buddy(self.auth)
		self.auth.remote(self.budy.afterLogin)
		self.talk = Talk(self, self.auth)
		self.auth.remote(self.talk.afterLogin)
		self.ch = Channel(self.auth)
		self.auth.remote(self.ch.afterLogin)
		self.call = Call(self.auth)
		self.auth.remote(self.call.afterLogin)
		self.poll = Poll(client_name)
		self.auth.remote(self.poll.afterLogin)
		self.liff = Liff(self.auth)
		self.auth.remote(self.liff.afterLogin)
		self.shop = Shop(self.auth)
		self.auth.remote(self.shop.afterLogin)
		self.tl = Timeline(self)
		self.auth.remote(self.tl.afterLogin)
		self._session = requests.Session()
		self.timelineHeaders = {}

	def __validate(self, name, token, mail, passwd, certt, qr):
		f = SyncAsync(self.auth.createLoginSession(name, token, mail, passwd, certt, qr)).run()
		if not f:
			return
		self.headers = {
				"User-Agent": self.auth.UA,
				"X-Line-Application": self.auth.LA,
				"X-Line-Access":self.auth.authToken.strip(),
			}
		
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try:
				setattr(self, k, v)
			except:
				pass
	
	def login(self, name=None, token=None, mail=None, passwd=None, certt=None, qr=False):
		self.__validate(name, token, mail, passwd, certt, qr)
		
	def save_file(self, path, raw):
		with open(path, "wb") as f:
			if isinstance(raw, HTTPResponse):
				shutil.copyfileobj(raw, f)
			else:
				f.write(raw)
		
	def delete_file(self, path):
		if os.path.exists(path):
			os.remove(path)
			return True
		else:
			return False
	
	def updateTimelineHeaders(self, obj):
		self.timelineHeaders.update(obj)
	
	def addTimelineHeader(self, keyval):
		self.timelineHeaders = keyval
			        
	async def get_content(self, url, headers=None, *args, **kwgs):
		if headers is None:
			headers = self.headers
		return self._session.get(url, headers=headers, stream=True, *args, **kwgs)
	
	async def post_content(self, url, data = None, files = None, headers = None, *args, **kwgs):
		if headers is None:
			headers = self.headers
		return self._session.post(url, data=data, files=files, headers=headers, *args, **kwgs)
	
	def generate_tempFile(self, returnAs='path'):
		assert returnAs in ['file','path'], 'Invalid returnAs value %s' % returnAs	
		fName, fPath = 'linesync-%s-%i.bin' % (int(time.time()), randint(0, 9)), tempfile.gettempdir()
		if returnAs == 'file':
			return fName
		elif returnAs == 'path':
			return os.path.join(fPath, fName)

	async def download_fileUrl(self, url, path=None, headers=None, return_as = "path", chunked=True):
		assert return_as in ['path','bool','bin'], 'Invalid returnAs value %' % return_as
		if not path:
			path = self.generate_tempFile()
		r = await self.get_content(url, headers=headers)
		if r.ok:
			if chunked:
				for chunk in r.iter_content(chunk_size=16*1024*1024):
					if chunk:
						self.save_file(path, chunk)
			else:
				self.save_file(path, r.raw)
			if return_as == "path":
				return path
			if return_as == "bin":
				return r.raw
			if return_as == "bool":
				return True
			else:
				logs.warning("args=(return_as), must be <bin or path or bool>, got {}".format(return_as))
		else:
			logs.error("Download url failed with code {}".format(r.status_code))
	
	def genOBSParams(self, newList, returnAs='json'):
		oldList = {'name': self.generate_tempFile('file'),'ver': '1.0'}
		assert returnAs in ['json','b64','default'], "Invalid parameter returnAs got %s" % returnAs
		if 'name' in newList and not newList['name']:
			newList['name'] = oldList['name']
		oldList.update(newList)
		if 'range' in oldList:
			new_range='bytes 0-%s\/%s' % (str(oldList['range']-1), str(oldList['range']))
			oldList.update({'range': new_range})
		if returnAs == 'json':
			return json.dumps(oldList)
		elif returnAs == 'b64':
			oldList=json.dumps(oldList)
			return base64.b64encode(oldList.encode('utf-8'))
		elif returnAs == 'default':
			return oldList
	
	async def downloadObjMessage(self,
								message_id,
								return_as = "path",
								path = None,
								remove_path = True,
								chunked=True):
		assert return_as in ["path", "bool"], "value of return_as incorrect got %s" % return_as
		if not path:
			path = self.generate_tempFile()	
		params = {"oid": message_id}
		uri = config.OBS_URL + '/talk/m/download.nhn?' + urllib.parse.urlencode(params)
		r = await self.get_content(uri)
		if r.ok:
			if chunked:
				for chunk in r.iter_content(chunk_size=16*1024*1024):
					if chunk:
						self.save_file(path, chunk)
			else:
				save_file(path, r.raw)
			if return_as == "path":
				return path
			elif return_as == "bool":
				return True
		else:
			logs.error("Download message content failed returning code %s" % r.status_code)
		if remove_path:
			self.delete_file(path)
	
	async def uploadObjHome(self, path, uri_img=None, type='image', returnAs='bool', objId=None):
		assert returnAs in ['objId','bool'], "Invalid returnAs value got %s" % returnAs
		assert type in ['image','video','audio'], "Invalid type value got %s" % type
		contentType = 'image/jpeg' if type == "image" \
								else 'video/mp4' if type == "video" \
								else 'audio/mp3' if type == "audio" else None
		if not objId:
			objId = int(time.time())
		file = open(path, 'rb').read()
		params = {
			'name': '%s' % str(time.time()*1000),
			'userid': '%s' % self.profile.mid,
			'oid': '%s' % str(objId),
			'type': type,
			'ver': '1.0'
			}
		headers = {}
		headers.update({
			'Content-Type': contentType,
			'Content-Length': str(len(file)),
			'x-obs-params': self.genOBSParams(params,'b64'),
			**self.timelineHeaders
		})
		r = await self.post_content(config.OBS_URL + '/myhome/c/upload.nhn', headers=headers, data=file)
		if not r.ok:
			raise Exception('Upload object home failure returning code %s' % r.status_code)
		if returnAs == 'objId':
			return objId
		elif returnAs == 'bool':
			return True
            
	async def uploadObjTalk(self, path, types='image', remove_path=False, objId=None, to=None, name=None):	
		assert types in ['image','gif','video','audio','file'], "values of types incorrect got %s" % types
		fdata = {"file": open(path, 'rb')}
		
		if types in ["image", "video", "file", "audio"]:
			headers = None
			uri = config.OBS_URL + '/talk/m/upload.nhn'
			data = {'params': self.genOBSParams({'oid': objId,'size': len(open(path, 'rb').read()),'type': types, 'name': name})}
		elif types == "gif":
			uri = config.OBS_URL + '/r/talk/m/reqseq'
			fdata = None
			data = open(path, 'rb').read()
			params = {
				'name': str(self.poll.revision - 1) + ".original",
				'oid': 'reqseq',
				'reqseq': str(self.poll.revision -1),
				'cat': 'original',
				'tomid': str(to), 
				'type': 'image',
				'ver': '1.0'
				}
			headers = {}
			headers.update({
				'X-Line-Carrier': '51089,1-0',
				'Content-Type': 'image/gif',
				'Content-Length': str(len(data)),
				'x-obs-params': self.genOBSParams(params,'b64'),
				**self.headers
			})
		
		r = await self.post_content(url=uri, data=data, files=fdata, headers=headers)
		if r.ok:
			return True
		else:
			logs.error("Upload content %s failed returning code %s" % (types, r.status_code))
		if remove_path:
			self.delete_file(path)
	
	async def updateGroupPicture(self,
							groupid,
							path = None,
							url = None,
							remove_path = True,
							chunked  = False) -> bool:
		"""
		Use this method to change group picture.
		
		Args:
			groupid: string of mid from group
			path: string from path that where file to upload
			url: string of image content to upload
			remove_path: bool pass True if want to deleted cache after download
		
		Return:
			<class 'bool'>
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use the path")
		if path is None and url is not None:
			path = await self.download_fileUrl(url, chunked=chunked)
		
		file = {'file': open(path, "rb")}
		data = {'params': self.genOBSParams({'oid': groupid,'type': 'image'})}
		uri = config.OBS_URL + '/talk/g/upload.nhn'	
		r = await self.post_content(url=uri, data=data, files=file)
		if r.ok:
			return True
		else:
			logs.error("Update group picture failed returning code %s" % r.status_code)
		if remove_path:
			self.delete_file(path)
	
	async def updateProfile(self,
						path = None,
						url = None,
						remove_path = True,
						type = "p",
						chunked = False) -> bool:
		"""
		Use this method to change group picture.
		
		Args:
			groupid: string of mid from group
			path: string from path that where file to upload
			url: string of image content to upload
			remove_path: bool pass True if want to deleted cache after download
			type: choose 'vp' if want to change video ad profile
			
		Return:
			<class 'bool'>
		"""
		if path is not None and url is not None:
			raise Exception("if args url is given, it cannot use path")
		if path is None and url is not None:
			path = await self.download_fileUrl(url, chunked=chunked)
		
		files = {'file': open(path, 'rb')}
		params = {'oid': self.mid,'type': 'image'}
		end = '/talk/p/upload.nhn'
		if type == "vp":
			params.update({'ver': '2.0', 'cat': 'vp.mp4'})
		data = {'params': self.genOBSParams(params)}
		uri = config.OBS_URL + end
		r = await self.post_content(url=uri, data=data, files=files)
		if r.ok:
			return True
		else:
			logs.error("Update profile failed returning code %s" % r.status_code)
		if remove_path:
			self.delete_file(path)
	
	async def updateProfileVideoPicture(self,
							uri_img = None,
							uri_vid = None,
							img_path=None,
							vid_path=None,
							chunked=False):
		vid_path = vid_path if vid_path else await self.download_fileUrl(uri_vid, chunked=chunked)
		img_path = img_path if img_path else await self.download_fileUrl(uri_img, chunked=chunked)
		files = {'file': open(vid_path, 'rb')}
		data = {'params': self.genOBSParams({'oid': self.profile.mid,'ver': '2.0','type': 'video','cat': 'vp.mp4'})}
		r_vp = await self.post_content(config.OBS_URL + '/talk/vp/upload.nhn', data=data, files=files)
		if r_vp.status_code != 201:
			raise Exception('Update profile video picture failure.')
		await self.updateProfile(path=img_path, type='vp', chunked=chunked)
	
	async def updateCover(self,
						path=None,
						uri_img=None,
						chunked=False,
						remove_path=True):
		await self.tl.updateToken()
		path = path if path else await self.download_fileUrl(uri_img, chunked=chunked)
		objId = await self.uploadObjHome(path=path, type="image", returnAs="objId")
		home = await self.tl.updateProfileCoverById(id=objId)
		return True