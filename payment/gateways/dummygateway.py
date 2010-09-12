from payment.gateways import GenericGateway

class DummyGateway( GenericGateway ):
	def process( self, transaction ):
		pass

	def authorize( self, transaction ):
		pass

	def capture( self, transaction ):
		pass

	def void( self, transaction ):
		pass

	def refund( self, transaction ):
		pass

	def credit( self, transaction ):
		pass

	def update( self, transaction ):
		pass
