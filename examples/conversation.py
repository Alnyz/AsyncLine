from AsyncLine import *
import asyncio

cl = Client('ios')
cl.login(name="mybot", qr=True)

data = {
	"name": None,
	"old": None,
}

@cl.hooks(type=26, filters=Filters.command("start") & Filters.private)
async def start_conversation(client, msg):
	await client.talk.sendMessage(msg.from_, "Hello stranger, what your name?")
	"""
	This method will be trigger conversation.
	Note: type must be 26 (Receive Message) and use this in private chat
		using Filters.private
	
	<func>:
		cl.poll.conversation(....
		args func:
			msg = (Message, require), Message from this comversation
			callback = (callable, require), function for next conversation
			done = (bool, optional), pass True if want this conversation ended
	"""
	client.poll.conversation(msg, callback_name)

async def callback_name(msg):
	data["name"] = msg.text
	await asyncio.sleep(1.3)
	await cl.talk.sendMessage(msg.from_, "Okay, now how old are you?")
	#done == True, after user send old this conversation will be ended
	cl.poll.conversation(msg, callback_old, done=True)

async def callback_old(msg):
	data["old"] = msg.text
	await cl.talk.sendMessage(msg.from_,
				"Nice too meet you, {} now i know your name and old {}".format(
					data["name"], data["old"]))

cl.poll.streams()