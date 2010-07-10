from payment.gateways import GenericGateway

class DummyGateway( GenericGateway ):
	def process( self, transaction=None, batch=None ):
		pass

	def authorize( self, transaction=None, batch=None ):
		pass

	def capture( self, transaction=None, batch=None ):
		pass

	def void( self, transaction=None, batch=None ):
		pass

	def refund( self, transaction=None, batch=None ):
		pass

	def credit( self, transaction=None, batch=None ):
		pass

	def update( self, transaction=None, batch=None ):
		pass
