from asyncio_monkey import patch_all # noqa isort:skip
patch_all()
from .f_LineService import Client as FLineServiceClient
from .f_LineService import Iface as FLineServiceIface
from .ttypes import *