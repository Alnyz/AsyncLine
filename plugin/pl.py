from AsyncLine import Client, Filters

@Client.hooks(type=26, filters=Filters.command("yoy"))
async def yoo(client, msg):
	await client.talk.sendMessage(msg.to, "yooy")
	
@Client.hooks(type=26, filters=Filters.command("yey"))
async def yey(client, msg):
	await client.talk.sendMessage(msg.to, "yeyy")
	
