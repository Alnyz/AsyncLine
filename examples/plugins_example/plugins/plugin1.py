from AsyncLine import Client, Filters

@Client.hooks(type=26, filters=Filters.command("heyo"))
async def heyho(client, msg):
	await client.talk.sendMessage(msg.to, "Heyhoo")
	
@Client.hooks(type=25, filters=lambda _,m: bool(m.text == "hei"))
async def hei(client, msg):
	"""
	filters lambda same as Filter class instance but you can overried it manually
	this new feature from AsyncLine.
	"""
	await client.talk.sendMessage(msg.param1, "hei")