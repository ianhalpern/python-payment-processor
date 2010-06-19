from payment.transactions import GenericTransaction
from payment.exceptions   import *

class CreditCard( GenericTransaction ):

	# Required
	card_number     = None
	expiration_date = None
	# Optional
	name            = None
	company         = None
	card_code       = None
	address         = None
	city            = None
	state           = None
	zip_code        = None
	phone           = None
	email           = None

	def __init__( self, amount, card_number=None, expiration_date=None,
	name=None, company=None, card_code=None, address=None, city=None,
	state=None, zip_code=None, phone=None, email=None ):

		GenericTransaction.__init__( self, amount, method='CC' )

		if not card_number or not expiration_date:
			raise TransactionInitializeError(
			  "TransactionCC requires both a 'card_number' and 'expiration_date' argument." )

		self.card_number     = card_number
		self.expiration_date = expiration_date
		self.name            = name
		self.company         = company
		self.card_code       = card_code
		self.address         = address
		self.city            = city
		self.state           = state
		self.zip_code        = zip_code
		self.phone           = phone
		self.email           = email
