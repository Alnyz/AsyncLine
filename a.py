from AsyncLine import *
from collections import defaultdict
from bs4 import BeautifulSoup as Soup
from subprocess import check_output, STDOUT, CalledProcessError, PIPE
import asyncio, uvloop, time, traceback, os, json

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

db = Storage(db_name="mydb", col_name="mycol", host="mongodb://bejo:aa9108lb@bejo-shard-00-00-0qffa.gcp.mongodb.net:27017/mydb?replicaSet=bejo-shard-0&retryWrites=true&w=majority")
cl = Client('ios', storage=db)
cl.login(name='heu', qr=True)


client = cl.talk
send = lambda i, t: SyncAsync(client.sendMessage(i, str(t))).run()

data = {
	"email": "",
	"passwd": None
}
async def stack_get(query, page=1):
	data = defaultdict(list)
	base_url = "http://stackoverflow.com"
	req = await cl.get_content(f'{base_url}/search?page={page}&q={query}', headers={})
	if req.ok:
		st = Soup(req.text, 'lxml').find_all('div',class_='question-summary search-result')
		for sup in st:
			data["url"].extend([base_url+i['href'] for i in sup.find_all('a',class_='question-hyperlink')])
			data["title"].extend([i.text.strip() for i in sup.find_all('a',class_='question-hyperlink')])
			data["excerpt"].extend([i.text.strip() for i in sup.find_all('div',class_='excerpt')])
			data["at"].extend([i.text.strip() for i in sup.find_all('div',class_='started fr')])
		return data

async def clb(msg):
	data["email"] = msg.text
	await client.sendMessage(msg.from_, "okay, send your password")
	cl.poll.conversation(msg, paswd)
	
async def paswd(msg):
	data["passwd"] = msg.text
	c = (await client.getContacts(msg.from_)).displayName
	tt = "Hey {} ini dia email dan password anda\n\nEmail: {}\nPassword:{}" \
		"apa anda yakin ini data anda? ya/tidak".format(
			c, data["email"], data["passwd"])
	await client.sendMessage(msg.from_, tt)
	cl.poll.conversation(msg, yakinn, done=True)
	
async def yakinn(msg):
	if msg.text.lower() == "ya":
		await client.sendMessage(msg.from_, "Mantap lurr")
	elif msg.text.lower() == "tidak":
		await client.sendMessage(msg.from_, "Anak tolol")
		
@cl.poll.hooks(type=26, filters=Filters.command("st") & Filters.private)
async def conv(msg):
	await client.sendMessage(msg.from_, "Hayy, Silahkan kirim email anda dahulu")
	cl.poll.conversation(msg, clb)
	
@cl.poll.hooks(type=25, filters=Filters.command('stackof'))
async def stackof(msg):
	if len(msg.command) <= 2:
		await client.sendMessage(msg.to, "ahh ..")
	text = msg.text.split()
	if 'num' in text:
		num = int(text.index('num'))
		n = text[num+1]
	if 'page' in text:
		page = int(text.index('page'))
	data = await stack_get(" ".join(text[1:num]), page = 1 if not 'page' in text else text[page+1])
	exc = data['excerpt'][int(n) - 1]
	title = data['title'][int(n) - 1]
	url = data['url'][int(n) - 1]
	at = data['at'][int(n) - 1]
	data = {
		'messages': [
			{
				'type': 'flex',
				'altText': 'Anu',
				'contents': {
					'type': 'carousel',
					'contents': [
						{
							'type': 'bubble',
							'header': {
								'type': 'box',
								'layout': 'vertical',
								'contents': [{
									'type': 'text',
									'text': title.lstrip("Q: "),
									'size': 'md',
									'weight': 'bold'
								},{
									'type': 'text',
									'text': at,
									'size': 'xs'
								}]
							},
							'body': {
								'type': 'box',
								'layout': 'vertical',
								'contents': [
									{
										'type': 'text',
										'text': exc.strip(),
										'wrap': True,
										'maxLines': 20 if len(exc) > 300 | 400 else 0
									},
									{'type': 'separator'},
									{
										'type': 'button',
										'height': 'sm',
										'action': {'type': 'uri', 'label': 'ReadMore', 'uri': url}
									}
								]
							}
						}
					]
				}
			}
		]
	}
	await cl.liff.sendFlex(msg.to, data)
	
@cl.poll.hooks(type=25, filters=Filters.command('stack'))
async def result_stack(msg):
	text  = msg.text.split()
	if 'page' in text:
		page = int(text.index('page'))
	sp = text[1:page] if 'page' in text else text[1:]
	data = await stack_get(" ".join(sp), page = 1 if not 'page' in text else text[page+1])
	title	= ["{}. {} ".format(i,v) for i, v in enumerate(data['title'], 1)]
	ret = "\n".join(str(v) for v in title)
	await client.sendMessage(msg.to, ret)
	
@cl.poll.hooks(type=25, filters=Filters.command("stest"))
async def spit(msg):
	t = time.time()
	await client.sendMessage(msg.to, "..")
	await client.sendMessage(msg.to, f"{time.time() - t}")

@cl.poll.hooks(type=25, filters=Filters.command("rb"))
async def restart(msg):
	await client.sendMessage(msg.to, 'Ikehhh')
	python = sys.executable
	os.execl(python, python, *sys.argv)
	
@cl.poll.hooks(type=25, filters=Filters.command('yo'))
async def bench(msg):
	t = time.time()
	ts = []
	await cl.talk.sendMessage(msg.to, "send 100 msg")
	for i in range(100):
		ts.append(client.sendMessage(msg.to, f'{i} at {time.time() - t}'))
	await asyncio.wait(ts)
	await client.sendMessage(msg.to, f'100 msg at {time.time() - t}')

@cl.poll.hooks(type=25, filters=Filters.command('$', prefix=""))
async def execute(msg):
	try:
		words = " ".join(msg.command[1:])
		answer = check_output([words], shell=True, stderr=STDOUT)
		a = answer.decode()
		await client.sendMessage(msg.to, str(a))
	except CalledProcessError as exc :
		e = exc.output.decode()
		await client.sendMessage(msg.to, str(e))
	except Exception:
		pass
		        
@cl.poll.hooks(type=25, filters=Filters.command("ex"))
async def ex(msg):
	tx = msg.text.split(None, 1)[1]
	try:
		with open('ex.py', 'w') as f:
			f.write(tx)
		with open('ex.py', 'r') as foo:
			exec(compile(open(foo.name).read(), foo.name, "exec"))
	except RuntimeError:
		pass
	except Exception:
		await client.sendMessage(msg.to, str(traceback.format_exc()))
		
cl.poll.streams()