from AsyncLine import *
from random import choice
import time

db = Storage(col_name="mycol", db_name="mydb", host="URI from mongodb apps")
"""
Ars Storage:
	col_name: (str | None, optional), create first collection for save data
	db_name: (str | None, optional), create first database for save Collection
	host: (str, Require), valid url from mongodb apps
"""
cl = LineNext("ios", storage=db)
cl.login(name="syncline")

@cl.poll.hooks(type=25, filters=Filters.command("yo") & Filters.mention)
async def _(msg):
	mid = await cl.talk.getMidWithTag(msg)
	data = []
	for i in mid:
		data.append({
			'name': (await cl.talk.getContacts(i)).displayName,
			'mid': i,
			'time': str(time.time())
			'role': choice(['admin', 'blacklist', 'whitelist', 'user']),
			'global': True
		})
	db.add_data(data=data)
	r = db.find_data(all=True)
	await cl.talk.sendMessage(msg.to, str(r))
	
cl.poll.streams()