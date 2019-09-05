from AsyncLine import *
import asyncio

cl = LineNext("ios")
cl.login(name="syncline", qr=True)

@cl.hooks(type=25, filters=Filters.command("gif"))
async def send_gif(client, msg):
	url = "your gif url here"
	await cl.talk.sendGif(msg.to, url=url)

@cl.hooks(type=25, filters=Filters.command("video") & Filters.group)
async def send_video(client, msg):
	"""
	This function for send video with text video using url which user at group
	args Filters.group change to Filters.private if want only send to private chat
	"""
	url = "your video url here"
	await client.talk.sendVideo(msg.to, url=url)
	
@cl.hooks(type=25, filters=Filters.command("image"))
async def send_image(client, msg):
	path = "path/to/your/inage.jpg/
	await client.talk.sendImage(msg.to, path=path, remove_path=True)

cl.poll.streams()