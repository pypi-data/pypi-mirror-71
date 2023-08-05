from ..Api		import StreamEndpoint, RequestType
from .template	import template
import json





class Stream ( StreamEndpoint ):
	_type		= RequestType.Quote
	_resource	= 'market/quotes.json'
	_method		= 'POST'
	_symbols	= []



	def req_body ( self, **kwargs ):
		"""Return get params together with post body data
		"""

		symbols	= kwargs.get('symbols',[])


		# Correctly format Symbols, also store split up symbols
		if type(symbols) == type(""):
			# We were passed string
			fmt_symbols = symbols
			symbols = symbols.split(',')
		else:
			# We were passed list
			fmt_symbols = ','.join(symbols)
			

			
		# Store symbols, so we can zip them back up with
		#  the response object
		symbols = [ s.upper() for s in symbols ]
		self._symbols = symbols

		# For aesthetics...
		fmt_symbols = fmt_symbols.upper()

		# Create request POST data
		data = { 'symbols':fmt_symbols }
			
		params = None
		return params, data








stream = template(Stream)
