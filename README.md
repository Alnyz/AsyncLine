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
- Safe-Thread thrift
- Slightly faster (make it sure)
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

client = LineNext('ios')
client.login(name='your session name')

#Run bot
loop = asyncio.get_event_loop()
loop.run_until_complete(client.poll.streams())
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
