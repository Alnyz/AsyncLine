from setuptools import setup

with open("README.md", "r") as f:
	long_description = f.read()
	
install_requires = [
	'frugal',
	'rsa',
	'ujson',
	'nats',
	'requests',
	'async_timeout',
	'aiohttp',
	'aiostomp',
	'asyncio-nats-client'
]

packages = [
	'LineSync',
]

setup(
	name='LineNext',
	version='1.3',
	long_description=long_description,
	long_description_content_type="text/markdown",
	description='LINE Unofficial Python Library with Asyncio support and C++ Binding',
	author="Anysz, Doodspav, Dyseo",
	author_email="katro.coplax@gmail.com",
	packages=packages,
	license='MIT',
	install_requires=install_requires,
	classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video"
    ]
)
