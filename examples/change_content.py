from AsyncLine import *
import asyncio

cl = Client("ios")
cl.login(name="syncline", qr=True)

trigger = {
	"changed":{}
}

@cl.hooks(type=25, filters=Filters.command("change profile", separator="\n"))
async def change_profile_picture(client, msg):
	"""
	This method to change your profile picture
	
	Args used: path as string where image store
	and then remove path after changing profile
	"""
	path = "your/path/to/image"
	await client.changeProfile(path=path, remove_path=True)
	
@cl.hooks(type=25, filters=Filters.command("change group pict", prefix="", separator="\n"))
async def change_group_profile_picture(client, msg):
	"""
	This method to change group picture
	
	Args used: url as string this url support content stream
	and then remove path after changing profile
	"""
	url = "url image content"
	await client.updateGroupPicture(msg.to, url=path, remove_path=True)

@cl.hooks(type=25, filters=Filters.command("change pict", separator="\n"))
async def triggerer(client, msg):
	trigger["changed"] = {msg.to: True}
	await client.talk.sendMessage(msg.to, "Gimme image for change group picture.")
	
@cl.hooks(type=25, filters=Filters.image)
async def change_with_trigger(client, msg):
	#check this group available for change pict
	if msg.to in trigger["changed"]:
		#check this group can changed
		if trigger["changed"][msg.to] == True:
			path = await cl.downloadObjMessage(msg.id)
			await client.updateGroupPicture(msg.to, path=path, remove_path=True)
			await client.talk.sendMessage(msg.to, "Success change group pictute")
			
cl.poll.streams()