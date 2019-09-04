from .filters import Filter
import AsyncLine

class BaseClient:
	def add_handler(self, *args, **kwgs):
		pass

class Handler:
    def __init__(self, callback: callable, filters=None):
        self.callback = callback
        self.filters = filters

class MessageHandler(Handler):
    def __init__(self, callback: callable, filters=None):
        super().__init__(callback, filters)
       
class HookMessage(BaseClient):
    def hooks(self=None, filters=None, type: int = 0):
        def decorator(func):
            if isinstance(self, AsyncLine.Client):
            	self.add_handler(MessageHandler(func, filters), type)
            elif isinstance(self, Filter) or self is None:
            	func.line_plugin = (
            		MessageHandler(func, filters), type)
            return func.line_plugin
        return decorator

class Methods(HookMessage):
	pass