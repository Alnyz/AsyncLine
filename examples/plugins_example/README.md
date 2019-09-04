## Pluging Guide
Hoowaaw!! Now you can use specified plugins directory for your main script

## How to
> `bot.py`

```python
from AsyncLine import Client
cli = Client('ios', plugins='plugins')
cli.login(name='sync', qr=True)

#your own script here

#now run
cli.poll.streams()
```

> `plugins` directory
this may look like this
```
├─ root     
    ├─ bot.py
    ├─ plugins
         ├─ plugin1.py
         ├─ other_plugin.py
         ├─ another_plugin.py
```

> `plugins/plugin1.py`
```python
from AsyncLine import Client, Filters

@Client.hooks(type=26, filters=Filters.command("heyo"))
async def heyho(client, msg):
	await client.talk.sendMessage(msg.to, "Heyhoo")	
```

> Note: this feature may effective if your using selfbot or only 1 bot
