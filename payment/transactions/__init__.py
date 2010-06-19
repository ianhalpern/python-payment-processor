from payment.exceptions import *

class GenericTransaction:
	__id__ = 0
	method = None
	amount = None

	def __init__( self, amount, method ):
		self.__class__.__id__ += 1
		self.__id__ = self.__class__.__id__
		self.method = method
		try:
			self.amount = float(amount)
		except ValueError:
			raise TransactionInitializeError( "'%s' is not a valid transaction amount." % amount )

