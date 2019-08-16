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

@cl.poll.hooks(type=25, filters=Filters.command("hello"))
async def send_message(msg):
	"""
	This function will wrap message text is it have 'hello' in text
	"""
	await cl.talk.sendMessage(msg.to, "Hello")

@cl.poll.hooks(type=25, filters=Filters.command("hey", prefix="."))
async def send_message(msg):
	"""
	This function will wrap message text is it have 'hey' in text with ("." prefix)
	"""
	name = (await cl.getContacts(msg._from)).displayName
	await cl.sendMessage(msg.to, "Hey "+name)

@cl.poll.hooks(type=13)
async def notifed_join(op):
	"""
	This function will wrap if some user join into group
	"""
	print(op)

@cl.poll.hooks(type=19)
async def notifed_kick(op):
	"""
	This function will wrap if some user have kicked
	"""
	print(op)
	

cl.poll.streams()
