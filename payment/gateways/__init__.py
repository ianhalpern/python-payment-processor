import types, urllib2, urllib
from payment.exceptions import *

def amountlimitcheck( method ):
	def amountlimitchecker( self, transaction, **kwargs ):
		kwargs['transaction'] = transaction
		if self.transaction_amount_limit != None and transaction.payment.amount > self.transaction_amount_limit:
			raise GatewayAmountLimitExceded(
			  "The transaction amount of '%d' excedes the gateway's limit of '%d' per transaction" %
			  ( transaction.payment.amount, self.transaction_amount_limit ) )

		return method( self, **kwargs )
	return amountlimitchecker

class GenericGateway( object ):

	transaction_amount_limit = None

	url = None
	api = {}

	def __new__( cls, *args, **kwargs ):
		if not hasattr( cls, '__clsinit__' ):
			cls.__clsinit__ = True
			cls.process = amountlimitcheck( cls.process )
			cls.capture = amountlimitcheck( cls.capture )
		return object.__new__(cls)

	def __init__( self, transaction_amount_limit=None ):
		if transaction_amount_limit != None:
			if transaction_amount_limit <= 0:
				raise GatewayInitializeError
			self.transaction_amount_limit = transaction_amount_limit

		self.api = self.newAPI() # creates a new api instance from the global api object

	def call( self, api ):
		post_str = '&'.join( [ k + '=' + urllib.quote( str(v) ) for k, v in api.items() if v != None ] )
		request  = urllib2.Request( self.url, post_str )
		response = urllib2.urlopen( request ).read()
		return response

	def newAPI( self ):
		return dict( self.api )

	# Authorize and capture a sale
	def process( self, transaction ):
		raise NotImplementedError

	# Authorize a sale
	def authorize( self, transaction ):
		raise NotImplementedError

	# Captures funds from a successful authorization
	def capture( self, transaction ):
		raise NotImplementedError

	# Void a sale
	def void( self, transaction ):
		raise NotImplementedError

	# Refund a processed transaction
	def refund( self, transaction ):
		raise NotImplementedError

	# Credits an account
	def credit( self, transaction ):
		raise NotImplementedError

	# Updates the order information for the given transaction
	def update( self, transaction ):
		raise NotImplementedError
