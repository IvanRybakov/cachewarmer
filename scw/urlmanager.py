import threading
import traceback
from crawler import Crawler

class URLManager(threading.Thread):
	def __init__(self, app):
		super(URLManager, self).__init__()
		self.app = app
		self.html_queue = []
		self.crawler = Crawler(app)

	def run(self):
		while (not self.app.getExitFlag() and self.app.enable_crawler):
			while (len(self.html_queue)):
				try:
					new_counter = 0
					(html, referer) = self.html_queue.pop()
					urls_list = self.crawler.parse_html(html, referer)
					for url in urls_list:
						if (self.app.add_url(url)):
							new_counter+=1
					self.app.printflush('Crawled URLs: ' + str(len(urls_list)) + ' new: ' + str(new_counter))
				except Exception as e:
					self.app.printflush( traceback.format_exc())
			
	def add_html_to_parse(self, html, referer):
		self.html_queue.append((html, referer))