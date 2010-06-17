
class GenericTransaction:
	method = None
	amount = None

	def __init__( self, amount, method ):
		self.method = method
		self.amount = amount
