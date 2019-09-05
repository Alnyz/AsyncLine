import asyncio
from AsyncLine import *

cl = Client('ios')
cl.login(name="syncline", qr=True)

@cl.hooks(type=25, filters=Filters.text)
async def echo_message(client, msg):
	"""
	This function will be catch all any message of text
	"""
	
	text = msg.text.lower()
	if text == "helo":
		await client.talk.sendMessage(msg.to, "Hello")
	if text == "hey":
		await client.talk.sendMessage(msg.to, "hey")

cl.poll.streams()