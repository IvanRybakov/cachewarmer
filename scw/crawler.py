from HTMLParser import HTMLParser
import urlparse

class Crawler(HTMLParser):
	def __init__(self, app):
		self.reset()
		self.app = app
		self.url_list = []
		self.referer = ''
		

	def handle_starttag(self, tag, attrs):
		if (tag == 'a'):
			for (attr_name, attr_value) in attrs:
				if (attr_name == 'href'):
					self.append_url_list(attr_value)
					break
		
	def parse_html(self, html, referer):
		self.url_list = []
		self.referer = referer
		self.feed(html)
		return self.url_list
		
	def append_url_list(self, url):
		normalized = self.normalize_url(url)
		if (normalized is not None):
			self.url_list.append(normalized) 

	def normalize_url(self, url):
		result = None
		ref_uri = urlparse.urlsplit(self.referer) #'{ref_uri.scheme}://{ref_uri.netloc}/{ref_uri.path}?{ref_uri.query}#{ref_uri.fragment}'.format(ref_uri=urlsplit(referer))
		parsed_uri = urlparse.urlsplit(url)
		if (parsed_uri.scheme in ['http', 'https'] and (parsed_uri.netloc == ref_uri.netloc or parsed_uri.netloc == '')):
			scheme = ref_uri.scheme if parsed_uri.scheme=='' else parsed_uri.scheme
			netloc = ref_uri.netloc if parsed_uri.netloc=='' else parsed_uri.netloc
			result = urlparse.SplitResult(scheme, netloc, parsed_uri.path, parsed_uri.query, None).geturl()
		return result
