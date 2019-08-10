from AsyncLine import *
import asyncio, time

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
	url = "https://r3---sn-2uuxa3vh-jb3k.googlevideo.com/videoplayback?expire=1564140612&ei=5I86XfOdJ8Xq1gLpuqeACg&ip=2001%3A1af8%3A4070%3Aa009%3A1%3A%3Affff&id=o-AFOtuJeWn0rx36TuZv_Q7oro18hpl-XSp99rXKIbHCaq&itag=18&source=youtube&requiressl=yes&mime=video%2Fmp4&gir=yes&clen=8791585&ratebypass=yes&dur=238.236&lmt=1552877694628337&fvip=5&c=WEB&txp=5531432&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=ALgxI2wwRQIhAP2zBci-d3eydmvQPYuupC2aw57vzdEYQ1SfqtZy5fg-AiB0bBUGmyX4Bp9n0IOntxrcf_yU3xMO1DwHh6UhEqo-LQ==&title=Westlife++-+You+Raise+Me+Up+-+Lyrics+%28Terjemahan%29&redirect_counter=1&rm=sn-aigesl76&req_id=c03cb2a1611ca3ee&cms_redirect=yes&ipbypass=yes&mip=110.138.150.39&mm=31&mn=sn-2uuxa3vh-jb3k&ms=au&mt=1564119012&mv=m&mvi=2&pl=26&lsparams=ipbypass,mip,mm,mn,ms,mv,mvi,pl&lsig=AHylml4wRgIhAMR1VmiREFUKzFe_mztjNy_MawYHHysnRrlg8Z1uKLPRAiEA_KtVwWli6ei1wUb6Tsp6iNhAXAGy1RDk7xNkg1ReYN0="
	await cl.talk.sendVideo(msg.to, url=url)
	
@cl.poll.hooks(type=25, filters=Filters.command("image"))
async def send_image(msg):
	path = "LINE.png"
	await cl.talk.sendImage(msg.to, path=path, remove_path=True)

print("Program Started")
print("Name: ",cl.profile.displayName)
cl.poll.streams()