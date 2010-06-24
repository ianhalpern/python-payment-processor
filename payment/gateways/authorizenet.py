# Authorize.net gateways

import urllib2, urllib

from payment.gateways   import GenericGateway
from payment.exceptions import *

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
		'x_login':    None,
		'x_tran_key': None,
		'x_test_request': 'FALSE',

		## Transaction Specific ##
		'x_type':       'AUTH_ONLY',
		'x_method':     'CC',
		'x_trans_id':    None,
		'x_auth_code':   None,
		'x_invoice_num': None,
		'x_description': None,
		'x_line_item':   None,
		'x_first_name':  None,
		'x_last_name':   None,
		'x_company':     None,
		'x_address':     None,
		'x_city':        None,
		'x_state':       None,
		'x_zip':         None,
		'x_country':     None,
		'x_phone':       None,
		'x_fax':         None,
		'x_email':       None,
		'x_cust_id':     None,
		'x_customer_ip': None
	}

	trans_id_cache = None

	def __init__( self, login=None, trans_key=None, use_test_url=False, **kwargs ):
		GenericGateway.__init__( self, **kwargs )

		if not login or not trans_key:
			raise GatewayInitializeError(
			  "The authorize.net gateway requires both a 'login' and 'trans_key' argument." )

		if use_test_url:
			self.url = URL_TEST

		self.trans_id_cache = {}

		self.api = dict( self.api )

		self.api['x_login']    = login
		self.api['x_tran_key'] = trans_key

	def call( self, transaction, api ):
		if transaction.method == 'CC':
			api['x_method']    = 'CC'
			api['x_amount']    = transaction.amount
			api['x_card_num']  = transaction.card_number
			api['x_exp_date']  = transaction.expiration_date.strftime( '%m-%Y' )
			api['x_card_code'] = transaction.card_code
			api['x_first_name']= transaction.first_name
			api['x_last_name'] = transaction.last_name
			api['x_address']   = transaction.address
			api['x_city']      = transaction.city
			api['x_state']     = transaction.state
			api['x_zip']       = transaction.zip_code
		else:
			raise PaymentMethodUnsupportedByGateway(
			  "Payment Method '%s' is unsupported by authorize.net AIM 3.1 gateway." % transaction.method )

		post_str = '&'.join( [ k + '=' + urllib.quote( str(v) ) for k, v in api.items() if v ] )
		request  = urllib2.Request( self.url, post_str )
		response = urllib2.urlopen( request ).read().split( api['x_delim_char'] )

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

		if response[0] != '1':
			# if response[0] == '2': # Declined
			#	raise ProcessingDeclined( response[3], error_code=response[2], avs_response=avs_response, ccv_response=ccv_response )
			# else: # 3 = Error, 4 = Held for review
			raise ProcessingError( response[3], error_code=int(response[2]), avs_response=avs_response, ccv_response=ccv_response  )

		if response[6] != '0':
			self.trans_id_cache[ transaction.__id__ ] = response[6] # transaction id
		return response[6]

	def process( self, transaction ):
		api = dict( self.api )

		if transaction.__id__ in self.trans_id_cache:
			api['x_type'] = 'PRIOR_AUTH_CAPTURE'
			api['x_trans_id'] = self.trans_id_cache[ transaction.__id__ ]
		else:
			api['x_type'] = 'AUTH_CAPTURE'

		return self.call( transaction, api )

	def authorize( self, transaction ):
		api = dict( self.api )
		api['x_type'] = 'AUTH_ONLY'

		return self.call( transaction, api )

	def capture( self, transaction, auth_code=None ):
		api = dict( self.api )
		api['x_type'] = 'CAPTURE_ONLY'

		if auth_code != None:
			api['x_auth_code'] = auth_code
		elif transaction.__id__ in self.trans_id_cache:
			api['x_type'] = 'PRIOR_AUTH_CAPTURE'
			api['x_trans_id'] = self.trans_id_cache[ transaction.__id__ ]

		return self.call( transaction, api )

	def refund( self, transaction, trans_id=None ):
		api = dict( self.api )
		api['x_type'] = 'CREDIT'

		if trans_id != None:
			api['x_trans_id'] = trans_id
		elif transaction.__id__ in self.trans_id_cache:
			api['x_trans_id'] = self.trans_id_cache[ transaction.__id__ ]

		return self.call( transaction, api )

	def void( self, transaction, trans_id=None ):
		api = dict( self.api )
		api['x_type'] = 'VOID'

		if trans_id != None:
			api['x_trans_id'] = trans_id
		elif transaction.__id__ in self.trans_id_cache:
			api['x_trans_id'] = self.trans_id_cache[ transaction.__id__ ]

		return self.call( transaction, api )
