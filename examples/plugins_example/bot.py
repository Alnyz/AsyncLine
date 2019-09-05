from AsyncLine import *

cl = Client("ios", plugins="plugins")
"""
Args:
	plugins: (str, optional) path to directort where plugins want to loaded
"""
cl.login(name="sync", qr=True)

@cl.hooks(type=25, filters=Filters.command("hey"))
async def _hai(client, msg):
	return


cl.poll.streams()