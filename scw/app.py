import sys

class App():
	def __init__(self):
		self.exit_flag = False
		self.IGNORE_EXIT_FLAG = True
		self.url_queue = []
		self.url_log = []
		self.enable_crawler = False

	def printflush(self, string, ignore_exit = False ):
		"""
		Print text and flush stdout
		"""
		if not self.getExitFlag() or ignore_exit == self.IGNORE_EXIT_FLAG:
			print str(string)
			sys.stdout.flush()
		
	def setExitFlag(self, exit_flag):
		self.exit_flag = exit_flag
		
	def getExitFlag(self):
		return self.exit_flag
		
	def deltaSeconds(self, delta):
		return float(delta.seconds) + float(delta.microseconds) / 1000000
		
	def add_url(self, url):
		"""
		Add new url to queue
		"""
		result = False
		if url not in self.url_queue and url not in self.url_log:
			self.url_queue.insert(0, url)
			result = True
		return result
			
	def get_url_queue(self):
		return self.url_queue
		
	def add_url_to_log(self, url):
		self.url_log.append(url)
	