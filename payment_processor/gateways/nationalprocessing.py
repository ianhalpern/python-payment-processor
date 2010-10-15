# NationalProcessing gateway

from payment_processor.gateways   import GenericGateway
from payment_processor.exceptions import *
import payment_processor.methods
import urlparse

class NationalProcessing( GenericGateway ):

	url = 'https://secure.nationalprocessinggateway.com/api/transact.php'

	api = {
		## Global ##

		## Instance Specific ##
		'username': None,
		'password': None,
		'dup_seconds':         None,     # Disable duplicates (in seconds)

		## Transaction Specific ##
		'type':               'auth',  # sale / auth / capture / void / refund / credit / update
		'payment':             None,   # creditcard / check
		'amount':              None,
		'sec_code':            'WEB', # PPD / WEB / TEL / CCD
		'processor_id':        None,
		'descriptor':          None,  # Set payment descriptor
		'descriptor_phone':    None,  # Set payment descriptor phone
		'validation':          None,  # Specify which Validation processors to use

		## CC Specific ##
		'ccnumber':            None,
		'ccexp':               None,  # MMYY
		'cvv':                 None,

		## Check Specific ##
		'checkname':           None,  # Name on bank account
		'checkaba':            None,
		'checkaccount':        None,
		'account_holder_type': None,  # business / personal
		'account_type':        None,  # checking / savings

		## Order Information ##
		'orderdescription':    None,
		'orderid':             None,
		'ponumber':            None,  # Original purchase order
		'tax':                 None,  # Total tax amount
		'shipping':            None,  # Total shipping amount
		#'product_sku_#':      None,  # Associate API call with Recurring SKU, replace # with an actual number

		## Customer Information ##
		'firstname':           None,
		'lastname':            None,
		'company':             None,
		'address1':            None,
		'address2':            None,
		'city':                None,
		'state':               None,
		'zip':                 None,
		'country':             'US',
		'phone':               None,
		'fax':                 None,
		'email':               None,
		'ipaddress':           None,

		## Shipping Information ##
		'shipping_firstname':  None,
		'shipping_lastname':   None,
		'shipping_company':    None,
		'shipping_address1':   None,
		'shipping_address2':   None,
		'shipping_city':       None,
		'shipping_state':      None,
		'shipping_zip':        None,
		'shipping_country':    'US',
		'shipping_email':      None
	}

	def __init__( self, username=None, password=None, **kwargs ):
		GenericGateway.__init__( self, **kwargs )

		if not username or not password:
			raise TypeError(
			  "The National Processing gateway requires both a 'username' and 'password' argument." )

		self.api['username'] = username
		self.api['password'] = password

	@GenericGateway.checkTransactionStatus
	def process( self, transaction, callback=None, async=False, api=None ):
		api = self.newAPI( api )

		api['type'] = 'sale'

		self.populateAPI( transaction, api )

		return self.call( transaction, api, callback, async )

	@GenericGateway.checkTransactionStatus
	def authorize( self, transaction, callback=None, async=False, api=None ):
		api = self.newAPI( api )

		api['type'] = 'auth'

		self.populateAPI( transaction, api )

		return self.call( transaction, api, callback, async )

	@GenericGateway.checkTransactionStatus
	def capture( self, transaction, callback=None, async=False, api=None ):
		if not transaction.payment.amount:
			raise ValueError( "National Processing's capture() requires a transaction with a defined payment amount." )

		api = self.newAPI( api )

		api['type']          = 'capture'
		api['transactionid'] = transaction.trans_id
		api['amount']        = transaction.payment.amount
		api['orderid']       = transaction.payment.order_number

		return self.call( transaction, api, callback, async )

	@GenericGateway.checkTransactionStatus
	def void( self, transaction, callback=None, async=False, api=None ):
		api = self.newAPI( api )

		api['type']          = 'void'
		api['transactionid'] = transaction.trans_id

		return self.call( transaction, api, callback, async )

	@GenericGateway.checkTransactionStatus
	def refund( self, transaction, callback=None, async=False, api=None ):
		api = self.newAPI( api )

		api['type']          = 'refund'
		api['transactionid'] = transaction.trans_id
		api['amount']        = transaction.payment.amount

		return self.call( transaction, api, callback, async )

	@GenericGateway.checkTransactionStatus
	def update( self, transaction, callback=None, async=False, api=None ):
		api = self.newAPI( api )

		api['type']          = 'update'
		api['transactionid'] = transaction.trans_id
		api['orderid']       = transaction.payment.order_number

		return self.call( transaction, api, callback, async )

	def handleResponse( self, transaction ):

		response = urlparse.parse_qs( transaction.last_response )

		response_code = int( response['response_code'][0] )
		response_text = response['responsetext'][0] + " (code %s)" % response_code

		print response
		if 'transactionid' in response:
			transaction.trans_id = response['transactionid'][0]

		transaction.last_response_text = response_text

		if response['response'][0] != '1':

			if response_code in ( 221, 222 ) or response_text.startswith('Invalid Credit Card Number'):
				raise InvalidCardNumber( response_text, response_code=response_code )

			if response_code in ( 223, 224 ):
				raise InvalidCardExpirationDate( response_text, response_code=response_code )

			if response_code in ( 225, ):
				raise InvalidCardCode( response_text, response_code=response_code )

			if response_text.startswith('Invalid ABA number'):
				raise InvalidRoutingNumber( response_text, response_code=response_code )

			if response_code in ( 0, ):
				raise InvalidAccountNumber( response_text, response_code=response_code )

			if 'avsresponse' in response and response['avsresponse'][0] in ( 'A', 'B', 'W', 'Z', 'P', 'L', 'N' ):
				if avs_response in ( 'A', ):
					raise InvalidBillingZipcode( response_text, response_code=response_code, avs_response=avs_response )

				raise InvalidBillingAddress( response_text, response_code=response_code, avs_response=avs_response )

			if response_code in ( 240, 250, 251, 252, 253, 260, 261, 262, 263, 264 ):
				raise TransactionDeclined( response_text, response_code=response_code )
			#print api
			# if response[0] == '2': # Declined
			#	raise ProcessingDeclined( response[3], error_code=response[2], avs_response=avs_response, ccv_response=ccv_response )
			# else: # 3 = Error, 4 = Held for review

			raise TransactionFailed( response_text, response_code=response_code )

	def populateAPI( self, transaction, api ):
		api['amount']    = transaction.payment.amount
		api['firstname'] = transaction.method.first_name
		api['lastname']  = transaction.method.last_name
		api['company']   = transaction.method.company
		api['address1']  = transaction.method.address
		api['address2']  = transaction.method.address2
		api['city']      = transaction.method.city
		api['state']     = transaction.method.state
		api['zip']       = transaction.method.zip_code
		api['phone']     = transaction.method.phone
		api['email']     = transaction.method.email

		api['orderdescription']   = transaction.payment.description
		api['orderid']            = transaction.payment.order_number
		api['ipaddress']          = transaction.payment.ip
		api['shipping_firstname'] = transaction.payment.ship_first_name
		api['shipping_lastname']  = transaction.payment.ship_last_name
		api['shipping_company']   = transaction.payment.ship_company
		api['shipping_address1']  = transaction.payment.ship_address
		api['shipping_city']      = transaction.payment.ship_city
		api['shipping_state']     = transaction.payment.ship_state
		api['shipping_zip']       = transaction.payment.ship_zip_code
		api['shipping_email']     = transaction.payment.ship_email

		if transaction.method.__class__ == payment_processor.methods.CreditCard:

			api['payment']   = 'creditcard'
			api['ccnumber']  = transaction.method.card_number
			api['ccexp']     = transaction.method.expiration_date.strftime( '%m-%Y' )
			api['cvv']       = transaction.method.card_code

		elif transaction.method.__class__ == payment_processor.methods.Check:

			api['payment']      = 'check'
			api['checkname']    = transaction.method.company \
								  or ( transaction.method.first_name or '' ) \
								  + ( ' ' + transaction.method.last_name if transaction.method.last_name else '' )
			api['checkaba']     = '%09d' % int( transaction.method.routing_number )
			api['checkaccount'] = transaction.method.account_number
			api['account_holder_type'] = transaction.method.account_holder_type
			api['account_type'] = transaction.method.account_type

		else:
			raise PaymentMethodUnsupportedByGateway(
			  "Payment Method '%s' is unsupported by authorize.net AIM 3.1 gateway." % transaction.method.__class__.__name__ )
