# -*- coding: utf-8 -*-
import asyncio
from AsyncLine import *

cl = LineNext('ios')
"""
LineNext(*args)
args:
	client_name: pass one of client name, see models.py
"""

cl.login(name="syncline")

cl.auth.url('/P4')

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


print("Program Started")
print("Name: ",cl.profile.displayName)

loop = asyncio.get_event_loop()
loop.run_until_complete(cl.poll.streams())
