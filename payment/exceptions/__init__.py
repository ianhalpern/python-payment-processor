class Error( Exception ):
	def __init__( self, reason, **kwargs ):
		for key, val in kwargs.items(): setattr( self, key, val )
		Exception.__init__( self, reason )

class NoGatewayError( Error ):
	"""Exception raised when the specified gateway does not exist"""
	pass

class GatewayAmountLimitExceded( Error ):
	pass

class PaymentMethodUnsupportedByGateway( Error ):
	"""Exception raised when the transaction method is unsupported by the gateway"""
	pass

class TransactionStatusError( Error ):
	"""Raised when a gateway cannot execute the desired payment function because of the payment's transaction status"""
	pass

class TransactionFailed( Error ):
	"""Explains any undefined error when processing a transaction"""
	pass

class TransactionDeclined( Error ):
	"""Raised when a transaction was declined though all fields were entered correctly, usually a result of insufficient funds."""
	pass

# All specific errors should be restricted to invalid user inputted fields
# that the developer cannot check beforehand like credit card number
# any other errors will be lumped into TransactionFailed

class InvalidCardNumber( Error ):
	pass

class InvalidCardExpirationDate( Error ):
	pass

class InvalidCardCode( Error ):
	pass

class InvalidRoutingNumber( Error ):
	pass

class InvalidAccountNumber( Error ):
	pass

class InvalidBillingAddress( Error ):
	pass

class InvalidBillingZipcode( Error ):
	pass

