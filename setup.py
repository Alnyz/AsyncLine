from setuptools import setup, find_packages
import sys

with open("README.md", encoding="utf-8") as f:
	long_description = f.read()

MINIMAL_PY_VERSION = (3, 7)

if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('asyncline works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

install_requires = [
	'frugal',
	'rsa',
	'ujson',
	'requests',
	'async_timeout',
	'aiohttp',
	'aiostomp',
	'asyncio-nats-client'
	'pymongo'
]

setup(
	name='AsyncLine',
	version='1.5.9.1',
	long_description=long_description,
	long_description_content_type="text/markdown",
	description='LINE Unofficial Python Library with Asyncio support and C++ Binding',
	author="Anysz, Doodspav, Dyseo",
	author_email="katro.coplax@gmail.com",
	packages=find_packages(exclude("examples", "examples")),
	url="https://github.com/dyseo/AsyncLine",
	download_url="https://github.com/dyseo/AsyncLine/releases/latest",
	license='MIT',
	requires_python='>=3.7',
	install_requires=install_requires,
	extras_require={
		'uvloop': ['uvloop==0.13.0']
	},
	classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
	"Framework :: AsyncIO",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
