import re
from payment.exceptions import *
from payment import methods

class Gateway( object ):
	'''The Gateway class is a wrapper around the gateways found in payment.gateways. It should be
	called with the name of the gateway as the first paramater. example: Gateway( 'authorize.net' )'''

	gateway = None

	def __init__( self, gateway_name, *args, **kwargs ):
		gateway_classname = ''.join([ s.capitalize() for s in re.split( '\W', gateway_name ) ])
		gateway_modulename = gateway_classname.lower()

		try:
			module = __import__( 'payment.gateways.%s' % gateway_modulename, fromlist=[ gateway_modulename ] )
			self.gateway = getattr( module, gateway_classname )( *args, **kwargs )
		except ImportError, AttributeError:
			raise NoGatewayError

	def __getattr__( self, value ):
		return getattr( self.__dict__['gateway'], value )

class PaymentInfo( object ):
	amount          = None
	order_number    = None
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

	def __init__( self, amount=None, order_number = None, description = None, ship_first_name = None, ship_company=None,
				  ship_last_name = None, ship_address = None, ship_address2 = None, ship_city = None, ship_state = None,
				  ship_zip_code = None, ship_country = None, ship_email = None, ship_phone = None, ip = None ):

		self.amount          = amount
		self.order_number    = order_number
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
	order   = None
	method  = None
	gateway = None

	trans_id = None

	def __init__( self, payment, method, gateway ):
		self.payment = payment
		self.method  = method
		self.gateway = gateway

	# Authorize and capture a sale
	def process( self ):
		self.gateway.process( self )

	# Authorize a sale
	def authorize( self ):
		self.gateway.authorize( self )

	# Captures funds from a successful authorization
	def capture( self ):
		self.gateway.capture( self )

	# Void a sale
	def void( self ):
		self.gateway.void( self )

	# Refund a processed transaction
	def refund( self ):
		self.gateway.refund( self )

	# Updates the order information for the given transaction
	def update( self ):
		self.gateway.update( self )
