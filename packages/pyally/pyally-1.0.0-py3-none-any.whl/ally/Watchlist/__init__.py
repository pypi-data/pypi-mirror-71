from collections.abc	import MutableMapping, MutableSet
from datetime			import datetime, timedelta
import weakref

from .methods import (
	GetWatchlist,
	GetWatchlists,
	CreateWatchlist,
	AppendWatchlist,
	DeleteWatchlist,
	DeleteFromWatchlist
)



class WatchlistWrapper ( MutableSet ):
	_name = ""
	_syms = set()

	def __init__ ( self, parent, name, symbols ):
		self._name = name
		self._syms = set(symbols)
		self._auth = weakref.ref(parent._auth())


	def __str__( self ):
		return str(self._syms)


	def __iter__ ( self ):
		return self._syms.__iter__()
	

	def __contains__ ( self, x ):
		return self._syms.contains(x)
	

	def __len__ ( self ):
		return self._syms.__len__()
	

	def add ( self, x ):
		if x not in self._syms:
			result = AppendWatchlist(
				auth				= self._auth(),
				watchlist_symbols	= x
			).request()

			
	def discard ( self, x ):
		if x in self._syms:
			result = DeleteFromWatchlist(
				auth				= self._auth(),
				watchlist_name		= self._name,
				watchlist_symbol	= x
			).request()
		






class Watchlist ( MutableMapping ):
	"""Handles a single remote watchlist instance.
	Can append to, view, or delete symbols
	"""
	_auth = None
	_expire = None


	def __getitem__ ( self, name ):
		result = GetWatchlist(
			auth			= self._auth(),
			watchlist_name	= name
		).request()

		return WatchlistWrapper( self, name, result )


	def __setitem__ ( self, name, symbols ):
		if type(symbols) != type([]):
			symbols = [str(symbols)]

		CreateWatchlist(
			auth				= self._auth(),
			watchlist_name		= name,
			watchlist_symbols	= symbols
		).request()


		
	def __delitem__ ( self, name ):
		DeleteWatchlist(
			auth				= self._auth(),
			watchlist_name		= name
		).request()
		

	
	@property
	def _all ( self ):
		"""Reusable way to get all watchlists
		"""
		t = datetime.now()

		if self._expire is None or self._expire < t:

			# Update cache
			self._expire = t + timedelta( seconds=0.75 )

			self._lists = GetWatchlists(
				auth = self._auth(),
			).request()

		return self._lists



	def __str__ ( self ):
		return str(self._all)
		
		

	def __iter__ ( self ):
		"""Return list to run over
		Must be wrapped in some special iterator stuff
		so that python3 will handle it how we want
		"""
		print("ITER")
		return self._all.__iter__()
	
	
		

	def __len__ ( self ):
		print("LEN")
		return len(self._all)




	def __init__ ( self, parent ):
		self._auth = weakref.ref(parent.auth)
		
	
