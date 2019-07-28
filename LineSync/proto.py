# -*- coding: utf-8 -*-
from frugal.protocol import FProtocol
class LegyProtocol(FProtocol):
	# We dont need frugal default body header
	def write_request_headers(self,*args,**kws):
		pass
	def write_response_headers(self,*args,**kws):
		pass
	def _write_headers(self, *args, **kws):
		pass
	def read_request_headers(self):
		pass
	def read_response_headers(self, *args, **kws):
		pass

class LegyProtocolFactory(object):
    def __init__(self, t_protocol_factory):
        """

        Args:
            t_protocol_factory: Thrift TProtocolFactory.
        """
        self._t_protocol_factory = t_protocol_factory

    def get_protocol(self, transport):
    	return LegyProtocol(self._t_protocol_factory.getProtocol(transport))
   
