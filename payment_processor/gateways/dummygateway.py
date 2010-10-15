from payment_processor.gateways import GenericGateway

class DummyGateway( GenericGateway ):

	def handleResponse( self, transaction ):
		pass

	@GenericGateway.checkTransactionStatus
	def process( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def authorize( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def capture( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def void( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def refund( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def credit( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )

	@GenericGateway.checkTransactionStatus
	def update( self, transaction, callback=None, async=False, api=None ):
		if callback: callback( transaction )
