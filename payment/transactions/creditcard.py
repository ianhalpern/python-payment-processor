from payment.transactions import GenericTransaction
from payment.exceptions   import *
import datetime

class CreditCard( GenericTransaction ):

	# Required
	card_number     = None
	expiration_date = None  # datetime.datetime or datetime.date
	# Optional
	first_name      = None
	last_name       = None
	company         = None
	card_code       = None
	address         = None
	city            = None
	state           = None
	zip_code        = None
	phone           = None
	email           = None

	def __init__( self, amount, card_number=None, expiration_date=None,
	first_name=None, last_name=None, company=None, card_code=None,
	address=None, city=None, state=None, zip_code=None, phone=None, email=None ):

		GenericTransaction.__init__( self, amount, method='CC' )

		if not card_number or not expiration_date:
			raise TransactionInitializeError(
			  "Credit Card transactions requires both a 'card_number' and 'expiration_date' argument." )

		if not isinstance( expiration_date, ( datetime.datetime, datetime.date ) ):
			raise TransactionInitializeError(
			  "Credit Card transactions require the 'expiration_date' argument to be of type 'datetime.datetime' or 'datetime.date'." )

		self.card_number     = card_number
		self.expiration_date = expiration_date
		self.first_name      = first_name
		self.last_name       = last_name
		self.company         = company
		self.card_code       = card_code
		self.address         = address
		self.city            = city
		self.state           = state
		self.zip_code        = zip_code
		self.phone           = phone
		self.email           = email

