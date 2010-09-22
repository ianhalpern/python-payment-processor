from payment_processor.exceptions   import *
import datetime

class GenericMethod:

	first_name = None
	last_name  = None
	company    = None
	card_code  = None
	address    = None
	address2   = None
	city       = None
	state      = None
	zip_code   = None
	country    = None
	phone      = None
	fax        = None
	email      = None

	def __init__( self, first_name=None, last_name=None, company=None, card_code=None,
				  address=None, address2=None, city=None, state=None, zip_code=None, country=None,
				  phone=None, fax=None, email=None ):

		self.first_name = first_name
		self.last_name  = last_name
		self.company    = company
		self.card_code  = card_code
		self.address    = address
		self.address2   = address2
		self.city       = city
		self.state      = state
		self.zip_code   = zip_code
		self.country    = country
		self.phone      = phone
		self.fax        = fax
		self.email      = email

class CreditCard( GenericMethod ):

	# Required
	card_number     = None
	expiration_date = None  # datetime.datetime or datetime.date

	# Optional
	card_code       = None

	def __init__( self, card_number=None, expiration_date=None, card_code=None, **kwargs ):

		GenericMethod.__init__( self, **kwargs )

		if not card_number or not expiration_date:
			raise TypeError(
			  "Credit Card method requires both a 'card_number' and 'expiration_date' argument." )

		if not isinstance( expiration_date, ( datetime.datetime, datetime.date ) ):
			raise ValueError(
			  "Credit method require the 'expiration_date' argument to be of type 'datetime.datetime' or 'datetime.date'." )

		self.card_number     = card_number
		self.expiration_date = expiration_date
		self.card_code       = card_code

class Check( GenericMethod ):

	CHECKING = 'checking'
	SAVINGS  = 'savings'
	PERSONAL = 'personal'
	BUSINESS = 'business'

	account_types        = ( CHECKING, SAVINGS )
	account_holder_types = ( PERSONAL, BUSINESS )

	account_number = None
	routing_number = None
	account_type   = None
	account_holder_type = None
	check_number = None

	def __init__( self, account_number=None, routing_number=None, account_type=CHECKING, account_holder_type=PERSONAL,
				  check_number = None, check_checkdigit=True, **kwargs ):

		GenericMethod.__init__( self, **kwargs )

		if not account_number or not routing_number:
			raise TypeError(
			  "Check method requires both an 'account_number' and 'routing_number' argument." )

		if not ( self.first_name and self.last_name ) and not self.company:
			raise TypeError(
			  "Check method requires either 'first_name' and 'last_name' arguments or 'company' argument." )

		if check_checkdigit and not self.validCheckdigit( routing_number ):
			raise ValueError(
			  "Invalid routing_number: checkdigit is invalid." )

		if account_type not in self.account_types:
			raise ValueError(
			  "Invalid account_type: Either '%s' required but '%s' was provided." % ( self.account_types, account_type ) )

		if account_holder_type not in self.account_holder_types:
			raise ValueError(
			  "Invalid account_holder_type: Either '%s' required but '%s' was provided." % ( self.account_holder_types, account_holder_type ) )

		self.account_number = account_number
		self.routing_number = routing_number
		self.account_type   = account_type
		self.account_holder_type = account_holder_type

	@classmethod
	def validCheckdigit( cls, routing_number, routing_number_length=9 ):
		'''Validates the routing number's check digit'''
		routing_number = str( routing_number ).rjust( routing_number_length, '0' )
		sum_digit = 0

		for i in range( routing_number_length - 1 ):
			n = int( routing_number[i:i+1] )
			sum_digit += n * (3,7,1)[i % 3]

		if sum_digit % 10 > 0:
			return 10 - ( sum_digit % 10 ) == int( routing_number[-1] )
		else:
			return not int( routing_number[-1] )

