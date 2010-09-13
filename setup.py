#!/usr/bin/python
from distutils.core import setup

setup(
	name         = 'payment_processor',
	version      = '0.2.0',
	description  = 'A simple payment gateway api wrapper',
	author       = 'Ian Halpern',
	author_email = 'ian@ian-halpern.com',
	url          = 'https://launchpad.net/python-payment',
	download_url = 'https://launchpad.net/python-payment/+download',
	packages     = ( 'payment_processor', 'payment_processor.gateways', 'payment_processor.methods', 'payment_processor.exceptions' )
)
