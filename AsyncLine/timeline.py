from .config import *
from .channel import Channel
from .models import *
import time
import urllib
import json

class Timeline(object):	
	def __init__(self, client):
		self.client = client
		
	def afterLogin(self, *args, **kws):
		for k,v in kws.items():
			try:
				setattr(self, k, v)
			except:
				pass
		self.client.updateTimelineHeaders({
			'Content-Type': 'application/json',
			'User-Agent': self.app_header[1],
			'X-Line-Carrier': '51089, 1-0',
			'X-Line-Mid': self.profile.mid,
			'X-Line-Application': self.app_header[0],
		})
	
	async def updateToken(self):
		self.client.updateTimelineHeaders({
			'X-Line-ChannelToken': (await self.client.ch.approveChannelAndIssueChannelToken('1341209850')).channelAccessToken
		})
	
	async def getFeed(self, postLimit=10, commentLimit=1, likeLimit=1, order='TIME'):
		await self.updateToken()
		params = {'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'order': order}
		url = TIMELINE_API+'/v45/feed/list.json?%s' % urllib.parse.urlencode(params)
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Getting feed failed with code % (%s)" % (r.status_code, r.text))
	
	async def getHomeProfile(self, mid=None, postLimit=10, commentLimit=1, likeLimit=1):
		await self.updateToken()
		if mid is None:
			mid = self.profile.mid
		params = {'homeId': mid, 'postLimit': postLimit, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'LINE_PROFILE_COVER'}
		url = TIMELINE_API+'/v45/post/list.json?%s' % urllib.parse.urlencode(params)
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Getting home failed with code % (%s)" % (r.status_code, r.text))
		
	async def getProfileDetail(self, mid=None):
		await self.updateToken()
		if mid is None:
			mid = self.profile.mid
		params = {'userMid': mid}
		url = TIMELINE_API+'/v1/userpopup/getDetail.json?userMid=%s' % mid
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Getting profile detail failed with code % (%s)" % (r.status_code, r.text))
	
	async def updateProfileCoverById(self, id, get=False):
		objId = await self.getProfileCoverID(id) if get else id
		params = {'coverImageId': objId}
		url = TIMELINE_API+'/v45/home/updateCover.json?%s' % urllib.parse.urlencode(params)
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Update cover failed with code % (%s)" % (r.status_code, r.text))
		
	async def getProfileCoverID(self, mid=None):
		if mid is None:
			mid = self.profile.mid
		home = await self.getProfileDetail(mid)
		return home['result']['objectId']
		
	async def getProfileCoverURL(self, mid=None):
		if mid is None:
			mid = self.profile.mid
		home = await self.getProfileDetail(mid)
		params = {'userid': mid, 'oid': home['result']['objectId']}
		return OBS_URL+'/myhome/c/download.nhn?%s' % urllib.parse.urlencode(params)

	async def createPost(self, text, holdingTime=None):
		await self.updateToken()
		params = {'homeId': self.profile.mid, 'sourceType': 'TIMELINE'}
		url = TIMELINE_API+'/v45/post/create.json?%s' % urllib.parse.urlencode(params)
		payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
		if holdingTime != None:
			payload["postInfo"]["holdingTime"] = holdingTime
		data = json.dumps(payload)
		r = await self.client.post_content(url, data=data, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Creating post failed with code % (%s)" % (r.status_code, r.text))

	async def createComment(self, postId, text, mid):
		await self.updateToken()
		params = {'homeId': mid, 'sourceType': 'TIMELINE'}
		url = TIMELINE_API+'/v45/comment/create.json?%s' % urllib.parse.urlencode(params)
		data = {'commentText': text, 'activityExternalId': postId, 'actorId': mid}
		r = await self.client.post_content(url, data=json.dumps(data), headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Creating comment failed with code % (%s)" % (r.status_code, r.text))
	
	async def deleteComment(self, postId, commentId, mid):
		await self.updateToken()
		params = {'homeId': mid, 'sourceType': 'TIMELINE'}
		url = TIMELINE_API+'/v45/comment/delete.json?%s' % urllib.parse.urlencode(params)
		data = {'commentId': commentId, 'activityExternalId': postId, 'actorId': self.profile.mid}
		r = await self.client.post_content(url, data=json.dumps(data), headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Deleting comment failed with code % (%s)" % (r.status_code, r.text))
	
	async def sendPostToTalk(self, mid, postId):
		await self.updateToken()
		params = {'receiveMid': mid, 'postId': postId}
		url = TIMELINE_API+'/v45/post/sendPostToTalk.json?%s' % urllib.parse.urlencode(params)
		r = await self.client.post_content(url, headers=self.client.timelineHeaders)
		return r.json()
	
	async def likePost(self, postId, mid, likeType=1005):
		await self.updateToken()
		if likeType not in [1001,1002,1003,1004,1005,1006]:
			raise Exception('Invalid parameter likeType')
		params = {'homeId': mid, 'sourceType': 'TIMELINE'}
		url = TIMELINE_API+'/v45/like/create.json?%s' % urllib.parse.urlencode(params)
		payload = {'likeType': likeType, 'activityExternalId': postId, 'actorId': mid}
		data = json.dumps(payload)
		r = await self.client.post_content(url, data=data, headers=self.client.timelineHeaders)
		return r.json()
	
	async def unlikePost(self, mid, postId):
		await self.updateToken()
		params = {'homeId': mid, 'sourceType': 'TIMELINE'}
		url = TIMELINE_API+'/v45/like/cancel.json?%s' % urllib.parse.urlencode(params)
		data = {'activityExternalId': postId, 'actorId': mid}
		r = await self.client.post_content(url, data=json.dumps(payload), headers=self.client.timelineHeaders)
		return r.json()
	
	async def getGroupPost(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
		await self.updateToken()
		params = {'homeId': mid, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'TALKROOM'}
		url = TIMELINE_API+'/v45/post/list.json?%s' % urllib.parse.urlencode(params)
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		return r.json()
	
	async def createGroupPost(self, mid, text):
		await self.updateToken()
		params = {'homeId': mid, 'sourceType': 'GROUP'}
		url = TIMELINE_API+'/v45/post/create.json?%s' % urllib.parse.urlencode(params)
		payload = {'postInfo': {'readPermission': {'type': 'ALL'}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
		data = json.dumps(payload)
		r = await self.client.post_content(url, data=data, headers=self.client.timelineHeaders)
		if r.ok:
			return r.json()
		raise Exception("Creating post group failed with code % (%s)" % (r.status_code, r.text))
		
	async def createGroupAlbum(self, mid, name):
		await self.updateToken()
		data = json.dumps({'title': name, 'type': 'image'})
		params = {'homeId': mid,'count': '1','auto': '0'}
		url = TIMELINE_MH+'/album/v3/album.json%s' % urllib.parse.urlencode(params)
		r = await self.client.post_content(url, data=data, headers=self.client.timelineHeaders)
		if not r.ok:
			raise Exception('Create a new album failure.')
		return r.json()
	
	async def getGroupAlbum(self, mid):
		await self.updateToken()
		params = {'homeId': mid, 'type': 'g', 'sourceType': 'GROUP'}
		url = TIMELINE_MH+'/album/v3/albums.json%s' % urllib.parse.urlencode(params)
		r = await self.client.get_content(url, headers=self.client.timelineHeaders)
		return r.json()
		