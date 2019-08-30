import asyncio
from AsyncLine import *

cl = Client('ios')
cl.login(name="syncline")

@cl.poll.hooks(type=25, filters=Filters.text)
async def echo_message(msg):
	"""
	This function will be catch all any message of text
	"""
	
	text = msg.text.lower()
	if text == "helo":
		await cl.talk.sendMessage(msg.to, "Hello")
	if text == "hey":
		await cl.talk.sendMessage(msg.to, "hey")

cl.poll.streams()