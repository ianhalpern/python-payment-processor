# Authorize.net gateways

from payment_processor.gateways   import GenericGateway
from payment_processor.exceptions import *
import payment_processor.methods

URL_STANDARD = 'https://secure.authorize.net/gateway/transact.dll'
URL_TEST     = 'https://test.authorize.net/gateway/transact.dll'

class AuthorizeNet():

	gateway = None

	def __init__( self, type='AIM', version='3.1', **kwargs ):

		if type == 'AIM' and version == '3.1':
			self.gateway = AuthorizeNetAIM_3_1( **kwargs )
		else:
			raise NoGatewayError(
			  "There is no authorize.net gateway with type '%s' and version '%s'." % ( type, version ) )

	def __getattr__( self, value ):
		return getattr( self.__dict__['gateway'], value )


class AuthorizeNetAIM_3_1( GenericGateway ):
	batch_support = False

	url = URL_STANDARD

	api = {
		## Global ##
		'x_delim_data':       'TRUE',
		'x_duplicate_window': '10',
		'x_delim_char':       '|',
		'x_relay_response':   'FALSE',
		'x_version':          '3.1',

		## Instance Specific ##
		'x_login':              None,
		'x_tran_key':           None,
		'x_test_request':      'FALSE',
		'x_allow_partial_Auth': None,
		'x_duplicate_window':   None, # Time limit duplicates can not be submitted: between 0 and 28800

		## Transaction Specific ##
		'x_type':              None,  # AUTH_CAPTURE (default), AUTH_ONLY, CAPTURE_ONLY, CREDIT, PRIOR_AUTH_CAPTURE, VOID
		'x_method':            None,  # CC or ECHECK
		'x_amount':            None,
		'x_recurring_billing': None,  # TRUE, FALSE,T, F, YES, NO, Y, N, 1, 0
		'x_trans_id':          None,
		'x_split_tender_id':   None,  # The payment gateway-assitned ID assigned when the original transaction includes  two or more partial payments.
		'x_auth_code':         None,  # The authorization code of an original transaction not authorized on the payment gateway

		## CC Specific ##
		'x_card_num':          None,
		'x_exp_date':          None,  # MMYY, MM/YY, MM-YY, MMYYYY, MM/YYYY, MM-YYYY
		'x_card_code':         None,
		'x_authentication_indicator': None,
		'x_cardholder_authentication_value': None,

		## ECHECK Specific ##
		'x_bank_aba_code':  None,
		'x_bank_acct_num':  None,
		'x_bank_name':      None,
		'x_bank_acct_name': None,  # CHECKING, BUSINESSCHECKING, SAVINGS
		'x_echeck_type':    None,  # ARC, BOC, CCD, PPD, TEL, WEB
		'x_bank_check_number': None,

		## Order Information ##
		'x_invoice_num':       None,
		'x_description':       None,
		'x_line_item':         None,
		'x_po_num':            None,

		## Customer Information ##
		'x_first_name':        None,
		'x_last_name':         None,
		'x_company':           None,
		'x_address':           None,
		'x_city':              None,
		'x_state':             None,
		'x_zip':               None,
		'x_country':           None,
		'x_phone':             None,
		'x_fax':               None,
		'x_email':             None,
		'x_cust_id':           None,
		'x_customer_ip':       None,

		## Shipping Information ##
		'x_ship_to_first_name': None,
		'x_ship_to_last_name':  None,
		'x_ship_to_company':    None,
		'x_ship_to_address':    None,
		'x_ship_to_city':       None,
		'x_ship_to_state':      None,
		'x_ship_to_zip':        None,
		'x_ship_to_country':    None,
		'x_tax':                None,
		'x_freight':            None,
		'x_duty':               None,
		'x_tax_exempt':         None

	}

	def __init__( self, login=None, trans_key=None, use_test_url=False, enable_test_requests=False, **kwargs ):
		GenericGateway.__init__( self, **kwargs )

		if not login or not trans_key:
			raise TypeError(
			  "The authorize.net gateway requires both a 'login' and 'trans_key' argument." )

		if use_test_url:
			self.url = URL_TEST

		if enable_test_requests:
			self.api['x_test_request'] = 'TRUE'

		self.api['x_login']    = login
		self.api['x_tran_key'] = trans_key

	@GenericGateway.checkTransactionStatus
	def process( self, transaction ):
		api = self.newAPI()

		api['x_type'] = 'AUTH_CAPTURE'

		self.populateAPI( transaction, api )

		return self.call( transaction, api )

	@GenericGateway.checkTransactionStatus
	def authorize( self, transaction ):
		api = self.newAPI()

		api['x_type'] = 'AUTH_ONLY'

		self.populateAPI( transaction, api )

		return self.call( transaction, api )

	@GenericGateway.checkTransactionStatus
	def capture( self, transaction ):
		api = self.newAPI()

		#if auth_code != None:
		#	api['x_type'] = 'CAPTURE_ONLY'
		#	api['x_auth_code'] = auth_code

		api['x_type']     = 'PRIOR_AUTH_CAPTURE'
		api['x_trans_id'] = transaction.trans_id

		return self.call( transaction, api )

	@GenericGateway.checkTransactionStatus
	def void( self, transaction ):
		api = self.newAPI()

		api['x_type']     = 'VOID'
		api['x_trans_id'] = transaction.trans_id

		return self.call( transaction, api )

	@GenericGateway.checkTransactionStatus
	def refund( self, transaction ):
		api = self.newAPI()

		api['x_type']     = 'CREDIT'
		api['x_trans_id'] = transaction.trans_id

		self.populateAPI( transaction, api )

		return self.call( transaction, api )

	def call( self, transaction, api ):

		response = GenericGateway.call( self, api ).split( api['x_delim_char'] )
		print response
		## Response ##
		#  0 - Response Code: 1 = Approved, 2 = Declined, 3 = Error, 4 = Held for Review
		#  1 - Response Subcode
		#  2 - Response Reason Code = http://developer.authorize.net/guides/AIM/Transaction_Response/Response_Reason_Codes_and_Response_Reason_Text.htm
		#  3 - Response Reason Text
		#  4 - Authorization Code
		#  5 - AVS Response
		#  6 - Transaction ID
		#  7 - Invoice Number
		#  8 - Description
		#  9 - Amount
		# 10 - Method
		# 11 - Transaction Type
		# 12 - 23 - Customer ID, First Name, Last Name, Company, Address, City, Sate, Zip, Country, Phone, Fax, Email
		# 24 - 31 - Ship First Name, Last Name, Company, Address, City, State, Zip, Country
		# 32 - Tax
		# 33 - Duty
		# 34 - Freight
		# 35 - Tax Exempt
		# 36 - Purchase Order Number
		# 37 - MD5 Hash
		# 38 - CCV Response
		# 39 - CAVV Response
		# 40 - Account Number
		# 41 - Card Type
		# 42 - Split Tender ID
		# 43 - Requested Amount
		# 44 - Balance on Card


		response_code = int(response[2])
		response_text = response[3] + " (code %s)" % response_code

		transaction.last_response_text = response_text

		if response[6] != '0':
			transaction.trans_id = response[6] # transaction id

		## AVS Response Code Values ##
		# A = Address (Street) matches, ZIP does not
		# B = Address information not provided for AVS check
		# E = AVS errorG = Non-U.S. Card Issuing Bank
		# N = No Match on Address (Street) or ZIP
		# P = AVS not applicable for this transaction
		# R = Retry - System unavailable or timed out
		# S = Service not supported by issuer
		# U = Address information is unavailable
		# W = Nine digit ZIP matches, Address (Street) does not
		# X = Address (Street) and nine digit ZIP match
		# Y = Address (Street) and five digit ZIP match
		# Z = Five digit ZIP matches, Address (Street) does not
		avs_response = response[5]

		# M = Match, N = No Match, P = Not Processed, S = Should have been present, U = Issuer unable to process request
		ccv_response = response[39]
		#print response[0], response[2]

		if response[0] != '1':

			if response_code in ( 6, 37, 200, 315 ):
				raise InvalidCardNumber( response_text, response_code=response_code )

			if response_code in ( 7, 8, 202, 316, 317 ):
				raise InvalidCardExpirationDate( response_text, response_code=response_code )

			if response_code in ( 44, 45, 65 ):
				raise InvalidCardCode( response_text, response_code=response_code )

			if response_code in ( 9, ):
				raise InvalidRoutingNumber( response_text, response_code=response_code )

			if response_code in ( 10, ):
				raise InvalidAccountNumber( response_text, response_code=response_code )

			if response_code in ( 27, 127, 290 ):
				if avs_response in ( 'A', ):
					raise InvalidBillingZipcode( response_text, response_code=response_code, avs_response=avs_response )

				raise InvalidBillingAddress( response_text, response_code=response_code, avs_response=avs_response )

			if response_code in ( 2, 3, 4, 41, 250, 251 ):
				raise TransactionDeclined( response_text, response_code=response_code )
			#print api
			# if response[0] == '2': # Declined
			#	raise ProcessingDeclined( response[3], error_code=response[2], avs_response=avs_response, ccv_response=ccv_response )
			# else: # 3 = Error, 4 = Held for review

			raise TransactionFailed( response_text, response_code=response_code )

		return response_text

	def populateAPI( self, transaction, api ):
		api['x_trans_id']    = transaction.trans_id
		api['x_amount']      = transaction.payment.amount

		api['x_first_name']  = transaction.method.first_name
		api['x_last_name']   = transaction.method.last_name
		api['x_company']     = transaction.method.company
		api['x_address']     = transaction.method.address
		if transaction.method.address2:
			api['x_address']+= ', ' + transaction.method.address2
		api['x_city']        = transaction.method.city
		api['x_state']       = transaction.method.state
		api['x_zip']         = transaction.method.zip_code
		api['x_country']     = transaction.method.country or api['x_country']
		api['x_fax']         = transaction.method.fax
		api['x_phone']       = transaction.method.phone
		api['x_email']       = transaction.method.email

		api['x_customer_ip'] = transaction.payment.ip
		api['x_cust_id']     = transaction.payment.customer_id
		api['x_invoice_num'] = transaction.payment.order_number
		api['x_description'] = transaction.payment.description

		api['x_ship_to_first_name'] = transaction.payment.ship_first_name
		api['x_ship_to_last_name']  = transaction.payment.ship_last_name
		api['x_ship_to_company']    = transaction.payment.ship_company
		api['x_ship_to_address']    = transaction.payment.ship_address
		if transaction.payment.ship_address2:
			api['x_ship_to_address'] += ', ' + transaction.payment.ship_address2
		api['x_ship_to_city']       = transaction.payment.ship_city
		api['x_ship_to_state']      = transaction.payment.ship_state
		api['x_ship_to_zip']        = transaction.payment.ship_zip_code
		api['x_ship_to_country']    = transaction.payment.ship_country

		if transaction.method.__class__ == payment.methods.CreditCard:

			api['x_method']    = 'CC'
			api['x_card_num']  = transaction.method.card_number
			api['x_exp_date']  = transaction.method.expiration_date.strftime( '%m-%Y' )
			api['x_card_code'] = transaction.method.card_code

		elif transaction.method.__class__ == payment.methods.Check:

			api['x_bank_aba_code'] = transaction.method.routing_number
			api['x_bank_acct_num'] = transaction.method.account_number

			api['x_bank_name']     = transaction.method.company \
								  or ( transaction.method.first_name or '' ) \
								  + ( ' ' + transaction.method.last_name if transaction.method.last_name else '' )

			api['x_bank_acct_name'] = 'CHECKING' if transaction.method.account_type == payment.methods.Check.CHECKING else 'SAVINGS'
			if transaction.method.account_holder_type == payment.methods.Check.BUSINESS:
				api['x_bank_acct_name'] = 'BUSINESS' + api['x_bank_acct_name']

			api['x_echeck_type'] = 'WEB'
			api['x_bank_check_number'] = transaction.method.check_number

		else:
			raise PaymentMethodUnsupportedByGateway(
			  "Payment Method '%s' is unsupported by authorize.net AIM 3.1 gateway." % transaction.method.__class__.__name__ )
