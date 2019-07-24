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

@cl.poll.hooks(25, Filters.text)
async def echo_message(op):
	m = op.message
	text = m.text.lower()
	if text == "helo":
		await cl.sendMessage(m.to, "Hello")
	if text == "hey":
		await cl.sendMessage(m.to, "hey")


print("Program Started")
print("Name: ",cl.profile.displayName)
if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(cl.poll.streams())