from AsyncLine import *
import asyncio

cl = LineNext("ios")
cl.login(name="syncline")

@cl.poll.hooks(type=25, filters=Filters.command("gif"))
async def send_gif(msg):
	url = "http://media1.giphy.com/media/kbusvRjNLcJmiTQ1os/200.gif"
	await cl.talk.sendGif(msg.to, url=url)

@cl.poll.hooks(type=25, filters=Filters.command("video") & Filters.group)
async def send_video(msg):
	"""
	This function for send video with text video using url which user at group
	args Filters.group change to Filters.private if want only send to private chat
	"""
	url = ""
	await cl.talk.sendVideo(msg.to, url=url)
	
@cl.poll.hooks(type=25, filters=Filters.command("image"))
async def send_image(msg):
	path = "path/to/your/inage.jpg/
	await cl.talk.sendImage(msg.to, path=path, remove_path=True)

cl.poll.streams()