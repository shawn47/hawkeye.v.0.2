#coding=utf-8

from datetime import datetime, timedelta
from db import CrawlerDB
from Logger import logger
from WordNetGenerator import wordNetGenerator
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import nltk
from NPExtractor import NPExtractor

DEFAULT_ANALYSIS_TIME_RANGE = 6

def newsTopicAnalysis(delta=DEFAULT_ANALYSIS_TIME_RANGE):
	logger.info("start to analysis from %s to %s." 
		% ((datetime.now() + timedelta(hours=-delta)).strftime("%Y-%m-%d %H:%M:%S"), 
			datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
	try:
		crawlerDB = CrawlerDB()
		
		fetchEndTime = (datetime.now() + timedelta(hours=-DEFAULT_ANALYSIS_TIME_RANGE)).strftime("%Y-%m-%d %H:%M:%S")
		newsList = crawlerDB.fetchNews(fetchEndTime)
		logger.info("total news number: %d" % len(newsList))
		
		# text = keywordExtractProcess(newsList)
		# wordNetGenerator(text)

		# text2 = keywordExtractProcess2(newsList)
		# wordNetGenerator(text2)

		text = keywordExtractProcess3(newsList)
		fileName = wordNetGenerator(text)
		return fileName, len(newsList)
	except Exception as e:
		logger.error("error: %s" % str(e))

None_Noun_Words = ["CD", "JJ", "JJR", "JJS", "VBG", "VBN", "VBP", "VB", "VBZ", "VBD", "DT", "TO", "IN", "RB"]
Filter_Word_Set = ["China", "china", "Chinese", "Beijing"]
Filter_Word_Set2 = ["world", "people", "time", "year", "percent", "new"]

def wordFilter(text):
	disease_List = nltk.word_tokenize(text)
	filtered = [w for w in disease_List if (w not in stopwords.words('english'))]
	rfiltered = nltk.pos_tag(filtered)
	rrfiltered = [w for w, tag in rfiltered if (tag not in None_Noun_Words) and (w not in Filter_Word_Set and w not in Filter_Word_Set2)]
	
	return " ".join(rrfiltered)

def wordFilterInPlace(text):
	for word in Filter_Word_Set:
		text = text.replace(word, "")
	# for word in Filter_Word_Set2:
	# 	text = text.replace(word, "")
	return text

def keywordExtractProcess3(newsList):
	textMerge = ""
	for news in newsList:
	    np_extractor = NPExtractor(wordFilterInPlace(news[6]))
	    result = np_extractor.extract()
	    textMerge += ",".join(result)
	return textMerge

def keywordExtractProcess2(newsList):
	textMerge = ""
	for news in newsList:
	    # np_extractor = NPExtractor(news[6])
	    # result = np_extractor.extract()
	    textMerge += wordFilter(news[6])
	return textMerge

def keywordExtractProcess(newsList):
	textMerge = ""
	for news in newsList:
	    # np_extractor = NPExtractor(news[6])
	    # result = np_extractor.extract()
	    textMerge += news[6]
	return textMerge

if __name__ == '__main__':
	newsTopicAnalysis(3)