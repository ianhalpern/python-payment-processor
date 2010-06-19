import types
from payment.exceptions import *

def checkinputs( method ):
	def inputchecker( self, transaction=None, batch=None, **kwargs ):
		if transaction:
			if not self.transaction_support: raise PaymentMethodUnsupportedByGateway( "Gateway does not support transaction payments." )
			kwargs['transaction'] = transaction
			if self.transaction_amount_limit != None and transaction.amount > self.transaction_amount_limit:
				raise GatewayAmountLimitExceded(
				  "The transaction amount of '%d' excedes the gateway's limit of '%d' per transaction" %
				  ( transaction.amount, self.transaction_amount_limit ) )

		if batch:
			if not self.batch_support: raise PaymentMethodUnsupportedByGateway( "Gateway does not support batch payments." )
			kwargs['batch'] = batch
			batch_amount = sum( [ t.amount for t in batch.transactions ] )
			if self.batch_amount_limit != None and batch_amount > self.batch_amount_limit:
				raise GatewayAmountLimitExceded(
				  "The batch amount of '%d' excedes the gateway's limit of '%d' per batch" %
				  ( batch_amount, self.batch_amount_limit ) )

		return method( self, **kwargs )
	return inputchecker

class GenericGateway( object ):

	transaction_support = True
	batch_support       = True

	transaction_amount_limit = None
	batch_amount_limit       = None

	def __new__( cls, *args, **kwargs ):
		if not hasattr( cls, '__clsinit__' ):
			cls.__clsinit__ = True
			for attr in GenericGateway.__dict__:
				if not attr.startswith( '__' ) and hasattr( cls, attr ) \
				and type( getattr( cls, attr ) ) == types.UnboundMethodType:
					setattr( cls, attr, checkinputs( getattr( cls, attr ) ) )
		return object.__new__(cls)

	def __init__( self, transaction_amount_limit=None, batch_amount_limit=None ):
		if transaction_amount_limit != None:
			if transaction_amount_limit <= 0:
				raise GatewayInitializeError
			self.transaction_amount_limit = transaction_amount_limit

		if batch_amount_limit != None:
			if batch_amount_limit <= 0:
				raise GatewayInitializeError
			self.batch_amount_limit = batch_amount_limit

	# Authorize and capture a sale
	def process( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Authorize a sale
	def authorize( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Captures funds from a successful authorization
	def capture( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Void a sale
	def void( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Refund a processed transaction
	def refund( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Credits an account
	def credit( self, transaction=None, batch=None ):
		raise MethodUndefinedError

	# Updates the order information for the given transaction
	def update( self, transaction=None, batch=None ):
		raise MethodUndefinedError
