# -*- coding: utf-8 -*-
from .models import *
from .auth import Auth
from .poll import Poll
from .talk import Talk
from .utils import ThreadPool
from . import config

from .lib.Gen.ttypes import *

from hyper.contrib import HTTPAdapter
from random import randint
from multiprocessing import Process
import os
import base64
import re
import requests
import shutil
import time
import json
import tempfile

def callback(*args, **kws):
	print(*args, **kws)

class LineNext(Talk):
	def __init__(self, client_name, workers=4):
		self.auth = Auth(client_name)
		self.auth.remote(self.afterLogin)
		super().__init__(self, self.auth)
		
		self.poll = Poll(client_name)
		self.auth.remote(self.poll.afterLogin)
			
		self._session = requests.Session()
		self._session.mount("https://", HTTPAdapter())
		self._session.mount("http://", HTTPAdapter())
		self.process = ThreadPool(workers)
		
	def __validate(self, mail, passwd, cert, token, qr):
		if mail is not None and passwd is not None and cert is None:
			SyncAsync(self.auth.loginWithCredential(mail, passwd, callback=callback)).run()
		elif mail is not None and passwd is not None and cert is not None:
			SyncAsync(self.auth.loginWithCredential(mail, passwd, cert, callback=callback)).run()
		elif token is not None:
			SyncAsync(self.auth.loginWithAuthToken(token)).run()
		elif qr is True:
			SyncAsync(self.auth.loginWithQrcode(callback=callback)).run()
		
		self.headers = {
				"User-Agent": self.auth.UA,
				"X-Line-Application": self.auth.LA,
				"X-Line-Access":self.auth.authToken
			}
	
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try: setattr(self, k, v)
			except: pass
			
	def login(self, mail=None, passwd=None, cert=None, token=None, qr=False):
		self.__validate(mail, passwd, cert, token, qr)
		
	def save_file(self, path, raw):
		with open(path, "wb") as f:
			f.write(raw)
		
	def delete_file(self, path):
		if os.path.exists(path):
			os.remove(path)
			return True
		else:
			return False
			        
	def get_content(self, url, headers=None, *args, **kwgs):
		if headers is None:
			headers = self.headers
		return self._session.get(url, headers=headers, stream=True, *args, **kwgs)
	
	def post_content(self, url, data = None, files = None, headers = None, *args, **kwgs):
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

	def download_fileUrl(self, url, path=None, headers=None, return_as = "path"):
		assert return_as in ['path','bool','bin'], 'Invalid returnAs value %' % return_as
		if not path:
			path = self.generate_tempFile()
			
		r = self.get_content(url, headers=headers, timeout=None)
		if r.ok:
			self.save_file(path, r.content)
			if return_as == "path":
				return path
			if return_as == "bin":
				return r.raw
			if return_as == "bool":
				return True
			else:
				raise TypeError("args=(return_as), must be <bin or path or bool>, got {}".format(return_as))
		else:
			raise Exception("Download url failed with code {}".format(r.status_code))
	
	def genOBSParams(self, newList, returnAs='json'):
		oldList = {'name': self.generate_tempFile('file'),'ver': '1.0'}
		if returnAs not in ['json','b64','default']:
			raise Exception('Invalid parameter returnAs')
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
	
	def uploadObjTalk(self, path, types='image', returnAs='bool', objId=None, to=None, name=None):
		if returnAs not in ['objId','bool']:
			raise Exception('Invalid returnAs value %s must objId or bool' % returnAs)
		if types not in ['image','gif','video','audio','file']:
			raise Exception('Invalid type value')
		
		headers=None
		fdata = {"file": open(path, 'rb')}
		if types in ["image", "video", "file", "audio"]:
			e_p = config.OBS_URL + '/talk/m/upload.nhn'
			data = {'params': self.genOBSParams({'oid': objId,'size': len(open(path, 'rb').read()),'type': types, 'name': name})}
		
		self.process.put(self.post_content,
						e_p, data,
						fdata, headers	
					)
		if path.endswith(".bin"):
			self.delete_file(path)