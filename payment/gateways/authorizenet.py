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

	def __init__( self, login=None, trans_key=None, test_url=False ):
		if not login or not trans_key:
			raise GatewayInitializeError(
			  "The authorize.net gateway requires both a 'login' and 'trans_key' argument." )

		if test_url:
			self.url = URL_TEST

		self.api = dict( self.api )

		self.api['x_login']    = login
		self.api['x_tran_key'] = trans_key

	def call( self, api ):
		post_str = '&'.join( [ k + '=' + urllib.quote( str(v) ) for k, v in api.items() if v ] )
		request  = urllib2.Request( self.url, post_str )
		response = urllib2.urlopen( request ).read()
		return response

	def authorize( self, transaction ):
		api = dict( self.api )

		api['x_type'] = 'AUTH_ONLY'

		if transaction.method == 'CC':
			api['x_method']    = 'CC'
			api['x_amount']    = transaction.amount
			api['x_card_num']  = transaction.card_number
			api['x_exp_date']  = transaction.expiration_date
			api['x_card_code'] = transaction.card_code
			api['x_zip']       = transaction.zip_code
		else:
			raise MethodUnsupportedByGateway(
			  "Method '%s' is unsupported by authorize.net AIM 3.1 gateway." % transaction.method )

		response = self.call( api )

		return response



"""
def call_auth( amount, card_num, exp_date, card_code, zip_code, request_ip=None ):
	'''Call authorize.net and get a result dict back'''
	import urllib2, urllib
	payment_post = dict( API )
	payment_post['x_amount'] = amount
	payment_post['x_card_num'] = card_num
	payment_post['x_exp_date'] = exp_date
	payment_post['x_card_code'] = card_code
	payment_post['x_zip'] = zip_code
	payment_request = urllib2.Request( url, urllib.urlencode(payment_post))
	r = urllib2.urlopen(payment_request).read()
	return r

def call_capture(trans_id): # r.split('|')[6] we get back from the first call, trans_id
	capture_post = API
	capture_post['x_type'] = 'PRIOR_AUTH_CAPTURE'
	capture_post['x_trans_id'] = trans_id
	capture_request = urllib2.Request( url, urllib.urlencode(capture_post))
	r = urllib2.urlopen(capture_request).read()
	return r
"""
