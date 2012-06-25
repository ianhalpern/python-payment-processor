from payment_processor.gateways import GenericGateway

class DummyGateway( GenericGateway ):

	def handleResponse( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def process( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def authorize( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def capture( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def void( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def refund( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def credit( self, transaction, api=None ):
		pass

	@GenericGateway.checkTransactionStatus
	def update( self, transaction, api=None ):
		pass
