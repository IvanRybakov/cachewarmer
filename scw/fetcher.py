from datetime import datetime
import threading
import urllib2 as ur
from urllib2 import HTTPError
import traceback

class Fetcher(threading.Thread):
	def __init__(self, app, url):
		super(Fetcher, self).__init__()
		self.app = app
		self.url = url
		self.load_time = 0.0
		self.code = None

	def run(self):
		try:
			try: 
				p_start = datetime.now()
				res = ur.urlopen(self.url)
				p_end = datetime.now()
				p_delta = p_end - p_start
				self.code = res.getcode()
			except HTTPError as http_error:
				p_end = datetime.now()
				p_delta = p_end - p_start
				self.code = http_error.code
			self.load_time = self.app.deltaSeconds(p_delta)
		except KeyboardInterrupt as e:
			self.app.setExitFlag(True)
			self.app.printflush( 'KeyboardInterrupt' + traceback.format_exc())
		except Exception as e:
			self.app.printflush( traceback.format_exc())
			
	def printStatus(self):
		self.app.printflush( str(format(self.load_time, '.3f')) + ' ' + str(self.code) + ' ' + self.url)