import newspaper
from newspaper import Article
from Logger import logger

class NewsFetcher(object):
	def __init__(self, url):
		self.url = url

	def fetch(self):
		article = Article(self.url, language='en')
		
		try:
			article.download()
			article.parse()

			authors = (article.authors)
			text = (article.text)
			article.nlp()
			keywords = article.keywords
			summary = article.summary
			return (authors, text, keywords, summary)
		except Exception as e:
			logger.error("newspaper download/parse error, url: %s, error info: %s" % (self.url, str(e)))
			return (None, None, None, None)
