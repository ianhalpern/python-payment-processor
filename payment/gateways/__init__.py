from exceptions import *

class GenericGateway():

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
