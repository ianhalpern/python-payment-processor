import types, urllib2, urllib
from payment_processor.exceptions import *
from payment_processor import Transaction

class GenericGateway( object ):

	transaction_amount_limit = None

	url = None
	api = {}

	def __new__( cls, *args, **kwargs ):
		if not hasattr( cls, '__clsinit__' ):
			cls.__clsinit__ = True
			cls.process = cls.checkAmountLimit( cls.process )
			cls.capture = cls.checkAmountLimit( cls.capture )
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

	@staticmethod
	def checkTransactionStatus( method ):
		def transactionStatusChecker( self, transaction, **kwargs ):

			if method.__name__ == 'process':
				if transaction.status != Transaction.PENDING:
					raise ValueError( "process() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.PENDING, transaction.status ) )

			if method.__name__ == 'authorize':
				if transaction.status != Transaction.PENDING:
					raise ValueError( "authorize() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.PENDING, transaction.status ) )

			if method.__name__ == 'capture':
				if transaction.status != Transaction.AUTHORIZED:
					raise ValueError( "capture() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.AUTHORIZED, transaction.status ) )

			if method.__name__ == 'void':
				if transaction.status != Transaction.AUTHORIZED:
					raise ValueError( "void() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.AUTHORIZED, transaction.status ) )

			if method.__name__ == 'refund':
				if transaction.status != Transaction.CAPTURED:
					raise ValueError( "refund() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.CAPTURED, transaction.status ) )

			if method.__name__ == 'update':
				if transaction.status != Transaction.AUTHORIZED:
					raise ValueError( "update() requires a transaction with a status of '%s', not '%s'."
					  % ( Transaction.AUTHORIZED, transaction.status ) )

			return method( self, transaction, **kwargs )
		return transactionStatusChecker

	@staticmethod
	def checkAmountLimit( method ):
		def amountLimitChecker( self, transaction, **kwargs ):
			if self.transaction_amount_limit != None and transaction.payment.amount > self.transaction_amount_limit:
				raise GatewayAmountLimitExceded(
				  "The transaction amount of '%d' excedes the gateway's limit of '%d' per transaction" %
				  ( transaction.payment.amount, self.transaction_amount_limit ) )

			return method( self, transaction, **kwargs )
		return amountLimitChecker

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
