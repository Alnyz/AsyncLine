# -*- coding: utf-8 -*-
import asyncio
from LineSync import *

cl = LineNext('ios')
"""
LineNext(*args)
args:
	client_name: pass one of client name, see models.py
	workers: int of workers for request
"""

cl.login(qr=True)
"""
Client.login(*args)
args:
	qr: bool pass True if wanna login with qr
	token: string pass a string token if have
	mail: string of email which registered on Line
	passwd: string of password from email registered
	cert: string cert after login email pass once if want login with cert
"""
cl.poll._thread = True
cl.poll._debug = False

cl.auth.url('/S4')

@cl.poll.hooks(25, Filters.command("hello"))
async def send_message(op):
	m = op.message
	text = m.text.lower()
	await cl.sendMessage(m.to, "Hello")

@cl.poll.hooks(25, Filters.command("hey", prefix="."))
async def send_message(op):
	m = op.message
	text = m.text.lower()
	name = (await cl.getContacts(m._from)).displayName
	await cl.sendMessage(m.to, "Hey "+name)

@cl.poll.hooks(13)
async def notifed_join(op):
	print(op)

@cl.poll.hooks(19)
async def notifed_kick(op):
	print(op)
	
print("Program Started")
print("Name: ",cl.profile.displayName)
if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(cl.poll.streams())