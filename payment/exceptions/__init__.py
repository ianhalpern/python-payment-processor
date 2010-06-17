class GatewayInitializeError( Exception ):
	"""Exception raised when a gateway cannot be initialized"""
	pass

class NoGatewayError( Exception ):
	"""Exception raised when the specified gateway does not exist"""
	pass

class NoTransactionError( Exception ):
	"""Exception raised when the specified transaction does not exist"""
	pass

class MethodUnsupportedByGateway( Exception ):
	"""Exception raised when the transaction method is unsupported by the gateway"""
	pass

class TransactionInitializeError( Exception ):
	"""Exception raised when a gateway cannot be initialized"""
	pass

class MethodUndefinedError( Exception ):
	"""Raised when a method is called by a class that hasn't implemented the
	method yet"""
	pass

class ProcessingError( Exception ):
	"""Explains an error in processing"""
	pass

class ProcessingDeclined( Exception ):
	"""A decline on card processing"""
	pass

class UnsupportedAmount( Exception ):
	"""An amount unsupported by the gateway has been specified"""
	pass

class RecurringUnsupported( Exception ):
	"""This is thrown whe recurring payments are requested from a gateway
	   without the capability of delivering them."""
	pass
