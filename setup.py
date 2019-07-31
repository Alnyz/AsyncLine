from setuptools import setup, find_packages

with open("README.md", "r") as f:
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

#packages = [
	#'AsyncLine',
	#'AsyncLine.lib',
#]

setup(
	name='AsyncLine',
	version='1.5.5',
	long_description=long_description,
	long_description_content_type="text/markdown",
	description='LINE Unofficial Python Library with Asyncio support and C++ Binding',
	author="Anysz, Doodspav, Dyseo",
	author_email="katro.coplax@gmail.com",
	packages=find_packages(),
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