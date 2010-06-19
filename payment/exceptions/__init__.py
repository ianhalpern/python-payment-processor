class Error( Exception ):
	def __init__( self, reason, **kwargs ):
		for key, val in kwargs.items(): setattr( self, key, val )
		Exception.__init__( self, reason )

class GatewayInitializeError( Error ):
	"""Exception raised when a gateway cannot be initialized"""
	pass

class TransactionInitializeError( Error ):
	"""Exception raised when a transaction cannot be initialized"""
	pass

class NoGatewayError( Error ):
	"""Exception raised when the specified gateway does not exist"""
	pass

class NoTransactionError( Error ):
	"""Exception raised when the specified transaction does not exist"""
	pass

class GatewayAmountLimitExceded( Error ):
	pass

class PaymentMethodUnsupportedByGateway( Error ):
	"""Exception raised when the transaction method is unsupported by the gateway"""
	pass

class MethodUndefinedError( Error ):
	"""Raised when a method is called by a class that hasn't implemented the
	method yet"""
	pass

class ProcessingError( Error ):
	"""Explains an error in processing"""
	pass

class ProcessingDeclined( Error ):
	"""A decline on card processing"""
	pass
