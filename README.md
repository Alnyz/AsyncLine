<p align="center">
    <a href="https://github.com/dyseo/AsyncLine">
        <img src="https://i.imgur.com/8yPDQiHr.png" alt="AsyncLine">
    </a>
    <br>
    <b>Line Messaging API for Python</b>
    <br>
    <a href="https://pypi.org/project/AsyncLine">
        PyPi
    </a>
    •
    <a href="https://github.com/dyseo/AsyncLine/releases">
        Releases
    </a>
    •
    <a href="https://line.me/ti/g2/KeQQBF78pOLSfe4uaS--Ew">
        Community
    </a>
</p>

<h3 align="center"> 
  <a href="https://python.org"> 
    <img src="https://img.shields.io/badge/3.6%20%7C%203.7-blue.svg?&logo=python&label=Python" alt="Python">
  </a>
  .
  <a href="https://opensource.org/licenses/MIT"> 
    <img src="https://img.shields.io/github/license/dyseo/A.svg" alt="License">
  </a>
  .
  <a href="https://travis-ci.org/dyseo/AsyncLine.svg?branch=master">
    <img src="https://travis-ci.org/dyseo/AsyncLine.svg?branch=master" alt="Build">
  </a>
  .
  <a href="https://github.com/dyseo/AsyncLine">
    <img src="https://img.shields.io/badge/Version-1.5.8-red" alt="Version">
  <a/>
</h3>
  

## Important
Please be warned: `AsyncLine` is in a very early beta. You will encounter bugs when using it. In addition, there are very many rough edges. With that said, please try it out in your applications: I need your feedback to fix the bugs and file down the rough edges.

## Features
- Fully Asynchronously
- Slightly faster
- Easy to use
- Documented
- Type-hint everywhere

## Installation
- `pip3 install AsyncLine --upgrade`

or clone this repository

1. `git clone https://github.com/dyseo/AsyncLine`
2. `cd AsyncLine`
3. `pip3 install -r requirements.txt`

## Simple usage
```python
from AsyncLine import LineNext
import asyncio

cli = LineNext('ios')
cli.login(name='your session name', qr=True)

"""
Args login:
	name: string for create new session for next login, no effect if using token login
	token: string of token for login using token, no need to create session name
	mail: string of email that using for login using email, you can pass name session for custom session
			default using string of email for name session
	passwd: password of email used
	cert: (string | optional) if you have cert pass at this args for easy login using email
			sure you can use custom session name for this too
	qr: boolean pass True if want to login using authQr, and you can use custom session name
		e.g client.login(name="sync", qr=True) this needed for next login
"""

@cli.hooks(type=26, filters=Filters.command("hello"))
async def hello_message(client, msg):
	await client.talk.sendMessage(msg.to, "Heyy!")
	
#Run bot
cli.poll.streams()
```
Please read [Example](examples) for more detail about usage this lib

## Author
Dyseo / [Line](https://line.me/ti/p/~line.bngsad)

## Base Source
Asynz / [Anysz](https://github.com/anysz)


## Getting Error
[Issues](https://github.com/dyseo/AsyncLine/issues) always open for this


## License
*AsyncLine* - Unofficially API Client library for Python

A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.

AsyncLine is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
