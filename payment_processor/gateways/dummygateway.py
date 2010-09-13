from payment_processor.gateways import GenericGateway

class DummyGateway( GenericGateway ):

	@GenericGateway.checkTransactionStatus
	def process( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def authorize( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def capture( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def void( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def refund( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def credit( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def update( self, transaction ):
		pass
