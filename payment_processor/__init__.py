import re
from payment_processor.exceptions import *
from payment_processor import methods

class Gateway( object ):
	'''The Gateway class is a wrapper around the gateways found in payment_processor.gateways. It should be
	called with the name of the gateway as the first paramater. example: Gateway( 'authorize.net' )'''

	gateway = None

	def __init__( self, gateway_name, *args, **kwargs ):
		gateway_classname = ''.join([ s.capitalize() for s in re.split( '\W', gateway_name ) ])
		gateway_modulename = gateway_classname.lower()

		try:
			module = __import__( 'payment_processor.gateways.%s' % gateway_modulename, fromlist=[ gateway_modulename ] )
			self.gateway = getattr( module, gateway_classname )( *args, **kwargs )
		except ImportError, AttributeError:
			raise NoGatewayError( "No gateway by the name '%s' exists." % gateway_name )

	def __getattr__( self, value ):
		return getattr( self.__dict__['gateway'], value )

class PaymentInfo( object ):
	amount          = None
	order_number    = None
	customer_id     = None
	description     = None
	ip              = None
	ship_first_name = None
	ship_last_name  = None
	ship_company    = None
	ship_address    = None
	ship_address2   = None
	ship_city       = None
	ship_state      = None
	ship_zip_code   = None
	ship_country    = None
	ship_email      = None
	ship_phone      = None

	def __init__( self, amount=None, order_number = None, customer_id = None, description = None, ship_first_name = None, ship_company=None,
				  ship_last_name = None, ship_address = None, ship_address2 = None, ship_city = None, ship_state = None,
				  ship_zip_code = None, ship_country = None, ship_email = None, ship_phone = None, ip = None ):

		self.amount          = amount
		self.order_number    = order_number
		self.customer_id     = customer_id
		self.description     = description
		self.ip              = ip
		self.ship_first_name = ship_first_name
		self.ship_last_name  = ship_last_name
		self.ship_address    = ship_address
		self.ship_city       = ship_city
		self.ship_state      = ship_state
		self.ship_zip_code   = ship_zip_code
		self.ship_country    = ship_country
		self.ship_email      = ship_email
		self.ship_phone      = ship_phone

class Transaction( object ):

	PENDING    = 'pending'
	AUTHORIZED = 'authorized'
	CAPTURED   = 'captured'
	VOIDED     = 'voided'
	REFUNDED   = 'refunded'

	status  = None
	status_pending = None

	payment = None
	method  = None
	gateway = None

	trans_id = None
	last_response = None
	last_response_text = None

	async = None
	callback = None

	def __init__( self, payment, method, gateway, status=PENDING, trans_id=None, callback=None, async=False ):
		self.payment = payment
		self.method  = method
		self.gateway = gateway

		self.status   = status
		self.trans_id = trans_id

		self.async = async
		self.callback = callback or self.__class__.handleResponse

	def handleResponse( self ):
		self.gateway.handleResponse( self )
		self.status = self.status_pending

	# Authorize and capture a sale
	def process( self, callback=None, async=None ):
		self.status_pending = Transaction.CAPTURED
		self.gateway.process( self, callback or self.callback, self.async if async is None else async )

	# Authorize a sale
	def authorize( self, callback=None, async=None ):
		self.status_pending = Transaction.AUTHORIZED
		self.gateway.authorize( self, callback or self.callback, self.async if async is None else async )

	# Captures funds from a successful authorization
	def capture( self, callback=None, async=None ):
		self.status_pending = Transaction.CAPTURED
		self.gateway.capture( self, callback or self.callback, self.async if async is None else async )

	# Void a sale
	def void( self, callback=None, async=None ):
		self.status_pending = Transaction.VOIDED
		self.gateway.void( self, callback or self.callback, self.async if async is None else async )

	# Refund a processed transaction
	def refund( self, callback=None, async=None ):
		self.status_pending = Transaction.REFUNDED
		self.gateway.refund( self, callback or self.callback, self.async if async is None else async )

	# Updates the order information for the given transaction
	def update( self, callback=None, async=None ):
		self.gateway.update( self, callback or self.callback, self.async if async is None else async )
