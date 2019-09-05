import asyncio
from AsyncLine import *

cl = Client('ios')
"""
LineNext(*args)
args:
	client_name: pass one of client name, see models.py
"""

cl.login(name="syncline", qr=True)

@cl.hooks(type=25, filters=Filters.command("hello"))
async def send_message(client, msg):
	"""
	This function will wrap message text is it have 'hello' in text
	"""
	await client.talk.sendMessage(msg.to, "Hello")

@cl.hooks(type=25, filters=Filters.command("hey", prefix="."))
async def send_message(client, msg):
	"""
	This function will wrap message text is it have 'hey' in text with ("." prefix)
	"""
	name = (await client.talk.getContacts(msg._from)).displayName
	await client.talk.sendMessage(msg.to, "Hey "+name)

@cl.hooks(type=13)
async def notifed_join(client, op):
	"""
	This function will wrap if some user join into group
	"""
	print(op)

@cl.hooks(type=19)
async def notifed_kick(client, op):
	"""
	This function will wrap if some user have kicked
	"""
	print(op)
	

cl.poll.streams()