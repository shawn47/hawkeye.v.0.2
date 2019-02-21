#coding=utf-8

from sys import argv
from SearchEngineNewsInfo import extractNewsByCountry
from NewsFetcher import NewsFetcher
from NPExtractor import NPExtractor
from utils import extractRelativeCountrys
from emailTools import roundSummaryInfoGenerator, tableRowContentGenerator, emailContentGenerator, sendMail, sendReportMail
from db import CrawlerDB
from Logger import logger
from NewsTopicAnalysis import newsTopicAnalysis

# return obj as:
# 	(title, news_hash, url, mediaInfo, rawTimeInfo, text)
def fetchNews(kw="china"):
	newsBasicInfo = extractNewsByCountry(kw)
	trContent = ""
	newsTextList = []
	for nbi in newsBasicInfo:
		newsFetcher = NewsFetcher(nbi[2])
		authors, text, keywords, summary = newsFetcher.fetch()
		newsTextList.append(text)
		if text != None:
			np_extractor = NPExtractor(text)
			kws_result = np_extractor.extract()
			trContent += tableRowContentGenerator(nbi[0], nbi[4], 
				nbi[2], ", ".join(extractRelativeCountrys(text)), summary)

	logger.info("++++++++++++")
	logger.info(newsBasicInfo)
	aggregateData = [ (t1 + (t2,))  for (t1, t2) in zip(newsBasicInfo, newsTextList)]

	return (aggregateData, trContent)

if __name__ == '__main__':
	script, method = argv
	# print(method)
	try:
		if method == "fetchNews":
			crawlerDB = CrawlerDB()
			kw = "china"
			aggregateData, trContent = fetchNews(kw)
			news_ID_list = crawlerDB.insertNewsBatch(aggregateData)
			logger.debug(news_ID_list)

			if method == "emailNotification":
				sendMail('News Collection', 
					emailContentGenerator(roundSummaryInfoGenerator(len(aggregateData)), trContent))
		elif method == "doReport":
			fileName, numberOfNews = newsTopicAnalysis(24)
			sendReportMail('News Report', fileName, numberOfNews)
		
	except Exception as e:
		logger.error("error: %s" % str(e))
