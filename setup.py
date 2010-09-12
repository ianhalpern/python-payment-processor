from distutils.core import setup

setup(
	name         = 'payment',
	description  = 'A simple payment gateway api wrapper',
	author       = 'Ian Halpern',
	author_email = 'ian@ian-halpern.com',
	url          = 'https://launchpad.net/python-payment',
	download_url = 'https://launchpad.net/python-payment/+download',
	packages     = ( 'payment', 'payment.gateways', 'payment.methods', 'payment.exceptions' )
)
