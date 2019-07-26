# -*- coding: utf-8 -*-
import asyncio
from LineSync import *

cl = LineNext('ios')
"""
LineNext(*args)
args:
	client_name: pass one of client name, see models.py
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

cl.auth.url('/P4')

@cl.poll.hooks(type=25, filters=Filters.text)
async def echo_message(msg):
	"""
	This function will be catch all any message of text
	"""
	
	text = msg.text.lower()
	if text == "helo":
		await cl.sendMessage(msg.to, "Hello")
	if text == "hey":
		await cl.sendMessage(msg.to, "hey")


print("Program Started")
print("Name: ",cl.profile.displayName)

loop = asyncio.get_event_loop()
loop.run_until_complete(cl.poll.streams())
