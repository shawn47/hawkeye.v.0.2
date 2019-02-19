#coding=utf-8

from sys import argv
from SearchEngineNewsInfo import extractNewsByCountry
from NewsFetcher import NewsFetcher
from NPExtractor import NPExtractor
from utils import extractRelativeCountrys
from emailTools import roundSummaryInfoGenerator, tableRowContentGenerator, emailContentGenerator, sendMail
from db import CrawlerDB
from Logger import logger

if __name__ == '__main__':
	script, method = argv
	# print(method)
	try:
		crawlerDB = CrawlerDB()
		kw = "china"
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
		news_ID_list = crawlerDB.insertNewsBatch(aggregateData)
		logger.debug(news_ID_list)
		sendMail('News Collection', 
			emailContentGenerator(roundSummaryInfoGenerator(len(newsBasicInfo)), trContent))
	except Exception as e:
		logger.error("error: %s" % str(e))
