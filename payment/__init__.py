import re
from payment.exceptions import *

class Gateway( object ):
	'''The Gateway class is a wrapper around the gateways found in payment.gateways. It should be
	   called with the name of the gateway as the first paramater. example: Gateway( 'authorize.net' )'''

	gateway = None

	def __init__( self, gateway_name, *args, **kwargs ):
		gateway_classname = ''.join([ s.capitalize() for s in re.split( '\W', gateway_name ) ])
		gateway_modulename = gateway_classname.lower()

		try:
			module = __import__( 'payment.gateways.%s' % gateway_modulename, fromlist=[ gateway_modulename ] )
			self.gateway = getattr( module, gateway_classname )( *args, **kwargs )
		except ImportError, AttributeError:
			raise NoGatewayError

	def __getattr__( self, value ):
		return getattr( self.__dict__['gateway'], value )

class Transaction( object ):

	transaction = None

	def __init__( self, transaction_name, *args, **kwargs ):
		transaction_classname = ''.join([ s.capitalize() for s in re.split( '\W', transaction_name ) ])
		transaction_modulename = transaction_classname.lower()

		try:
			module = __import__( 'payment.transactions.%s' % transaction_modulename, fromlist=[ transaction_modulename ] )
			self.transaction = getattr( module, transaction_classname )( *args, **kwargs )
		except ImportError, AttributeError:
			raise NoTransactionError

	def __getattr__( self, value ):
		return getattr( self.__dict__['transaction'], value )


class Batch:
	transactions = []

