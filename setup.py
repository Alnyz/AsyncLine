#import cmarkgfm
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
	long_description = f.read()

install_requires = [
	'frugal',
	'rsa',
	'ujson',
	'requests',
	'async_timeout',
	'aiohttp',
	'aiostomp',
	'asyncio-nats-client'
]

setup(
	name='AsyncLine',
	version='1.5.8.3',
	long_description=long_description,
	long_description_content_type="text/markdown",
	description='LINE Unofficial Python Library with Asyncio support and C++ Binding',
	author="Anysz, Doodspav, Dyseo",
	author_email="katro.coplax@gmail.com",
	packages=find_packages(),
	url="https://github.com/dyseo/AsyncLine",
	download_url="https://github.com/dyseo/AsyncLine/releases/latest",
	license='MIT',
	install_requires=install_requires,
	classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)