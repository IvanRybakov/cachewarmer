
import urllib2 as ur
import re, traceback
import sys
import os

from scw.fetcher import Fetcher
from scw.app import App
from scw.urlmanager import URLManager


class CacheWarmer():
	def __init__(self, sitemap, processes = 100):
		self.processes = processes
		self.active_threads = []
		self.app = App()
		self.updated_count = 0
		self.fetched_count = 0
		self.sitemap_url = sitemap
		self.code_statistics = {}
		self.average_time = 0.0
		self.url_manager = URLManager(self.app)

	def start(self):
		"""
		Execute the main process
		"""
		self.app.printflush('Sitemap: ' + self.sitemap_url)
		self.getUrlsList()
		self.app.printflush('Fetched: ' + str(self.fetched_count))
		self.app.printflush('Processes: ' + str(self.processes))
		self.CheckURLs()
		self.printReport()
		
	def printReport(self):
		"""
		Print a report after process execution
		"""
		self.app.printflush('Fetched: ' + str(self.fetched_count), self.app.IGNORE_EXIT_FLAG)
		self.app.printflush('Processes: ' + str(self.processes), self.app.IGNORE_EXIT_FLAG)
		self.app.printflush('Updated: ' + str(self.updated_count), self.app.IGNORE_EXIT_FLAG)
		self.app.printflush('Average page load time: ' + str(self.average_time), self.app.IGNORE_EXIT_FLAG)
		self.app.printflush('Returned with code: ' + repr(self.code_statistics), self.app.IGNORE_EXIT_FLAG)
		self.app.printflush('Closing Processes... ', self.app.IGNORE_EXIT_FLAG)

	def getUrlsList(self):
		"""
		Fetch an URLs list from website XML sitemap
		"""
		try:
			f = ur.urlopen(self.sitemap_url)
			res = f.readlines()
			for d in res:
			  data = re.findall('<loc>(https?:\/\/.+?)<\/loc>',d)
			  for url in data:
				self.app.add_url(url)
		except Exception as e:
			self.app.printflush(str(e))
			self.app.printflush(traceback.format_exc())
		self.fetched_count = len(self.app.get_url_queue())


	def CheckURLs(self):
		"""
		Start multy-threading requests to website
		"""
		self.updated_count = 0
		self.app.setExitFlag(False)
		if (self.app.enable_crawler):
			self.app.printflush('Crawler enabled!')
			self.url_manager.start()
		try:
			parsed_params = self.app.get_url_queue()
			while (parsed_params):
				self.active_threads = []
				while True:
					while len(self.active_threads) < self.processes and len(parsed_params) > 0:
						urlItem = parsed_params.pop()
						if urlItem != None:
							self.app.add_url_to_log(urlItem)
							thread = Fetcher(self.app, urlItem)
							thread.start()
							self.active_threads.append( thread )
					if self.app.getExitFlag():
						break
					if len( self.active_threads ) == 0:
						break
					else:
						for thread in self.active_threads:
							if not thread.isAlive():
								self.url_manager.add_html_to_parse(thread.html, thread.url)
								thread.printStatus()
								self.collectStat(thread)
								self.active_threads.remove(thread)
				if self.app.getExitFlag():
					break
		except KeyboardInterrupt as e:
			self.app.printflush('KeyboardInterrupt')
		except Exception as e:
			self.app.printflush(traceback.format_exc())
		self.app.setExitFlag(True)
			
	def collectStat(self, thread):
		"""
		Collect statistic for a request
		"""
		# update average page load time
		if self.updated_count == 0:
			self.average_time = thread.load_time
		else:
			self.average_time = (self.average_time * self.updated_count + thread.load_time) / (self.updated_count + 1)
		# update stitistics by HTTP code
		if thread.code not in self.code_statistics:
			self.code_statistics[thread.code] = 1 
		else:
			self.code_statistics[thread.code] += 1
		# update count of processed pages
		self.updated_count += 1
