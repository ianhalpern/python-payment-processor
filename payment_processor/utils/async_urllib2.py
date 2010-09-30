import urllib2, threading

_thread = None

queue = []

def urlopen( request, callback ):
	global _thread

	queue.append( ( request, callback ) )

	if not _thread:
		_thread = threading.Thread( target=_requestThread )
		_thread.start()

def _requestThread():
	global _thread

	while len( queue ):
		request, callback = queue.pop()
		response = urllib2.urlopen( request ).read()
		callback( response )

	_thread = None
