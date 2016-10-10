import threading
import urllib2 as ur
import re, traceback
import sys

MAX_PROCESS_COUNT = 100

def getUrlsList():
	try:
		f = ur.urlopen(u'https://site/sitemap.xml')
		res = f.readlines()
		urlsList = []
		for d in res:
		  data = re.findall('<loc>(https?:\/\/.+)<\/loc>',d)
		  for i in data:
			urlsList.append(i)
		print "Fetched pages: ", len(urlsList)
		sys.stdout.flush()
		return urlsList
	except Exception as e:
		print str(e)
		print traceback.format_exc()
		sys.stdout.flush()


def CheckURLs(urls):
	"""
	Start multy-threading requests to AN
	"""
	_updated = 0
	EXIT_FLAG = False
	try:
		parsed_params = urls
		messages = []
		__activeThreads = []
		while (parsed_params):
			messages = []
			__activeThreads = []
			while True:
				while len(__activeThreads) < MAX_PROCESS_COUNT and len(parsed_params) > 0:
					urlItem = parsed_params.pop()
					if urlItem != None:
						thread = Fetcher(urlItem)
						thread.start()
						__activeThreads.append( thread );
				if EXIT_FLAG:
					print 'EXITING... '
					sys.stdout.flush()
					break
				if len( __activeThreads ) == 0:
					break
				else:
					for thread in __activeThreads:
						if not thread.isAlive():
							_updated += 1
							__activeThreads.remove(thread)
	except KeyboardInterrupt as e:
		print 'KeyboardInterrupt' + traceback.format_exc()
		EXIT_FLAG = True
		self.response = {'status':'error', 'message': repr(e)}
	except Exception as e:
		print traceback.format_exc()
	print 'Fetched ' + str(_updated)


class Fetcher(threading.Thread):
	def __init__(self, url):
		threading.Thread.__init__(self)
		self.url = url
		self.response = ""
		self.result = None

	def run(self):
		try:
			ur.urlopen(self.url)
			print self.url
			sys.stdout.flush()
		except KeyboardInterrupt as e:
			print 'KeyboardInterrupt' + traceback.format_exc()
			sys.stdout.flush()
			EXIT_FLAG = True
			self.response = {'status':'error', 'message': repr(e)}
		except Exception as e:
			print traceback.format_exc()
			sys.stdout.flush()
			self.response = {'status':'error', 'message': repr(e)}
		return

CheckURLs(getUrlsList())