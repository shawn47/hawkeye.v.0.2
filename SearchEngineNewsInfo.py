#coding=utf-8

from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from Logger import logger
from datetime import datetime, timedelta
import string
import os
import re
import urllib
import hashlib
import time

from user_agents import user_agents
from config import URL_NEXT
from utils import urlFilter, extractMediaExpireDate, getRandomDomain, getRandomUserAgent

def requestAssemblor(searchWord):
	domain = getRandomDomain()
	url = URL_NEXT
	url = url.format(domain = domain, query = searchWord.strip(), num = 30, qdr = 'n30')
	request = quote(url, safe = string.printable)
	logger.info(request)

	user_agent = getRandomUserAgent()
	headers = {
		'User-Agent': user_agent,
		'cookie': 'NID=126=rHiwWGEfr2VVtMOVvfLbZUa1FnGmWEo01MZlNN9DGJjGzdLfF342sf9gwVk8sGqQJUVWB8pp7d2Cpih9DUinHM17ITBtnmxGFVpC0Zz-8D0jCWnjIUSgLYCrBUP1bQVg9pHLyFQ; DV=c1EnZfFkERoSYKEIkm8vVLY3NacHJxY; 1P_JAR=2018-3-29-6'
		}
	req = urllib.request.Request(url = request, headers = headers)
	try:
		response = urllib.request.urlopen(req)
		soup = BeautifulSoup(response.read(), features="lxml")
	except Exception as e:
		logger.error(e)
		logger.error("unavailable doamin: %s" % domain)
		soup = requestAssemblor(searchWord)

	return soup

def extractNewsByCountry(keyWord):
	keyWordArr = keyWord.split(" ")
	searchWord = keyWordArr[0]
	countryA = None if len(keyWordArr) < 2 else keyWordArr[1]
	countryB = None if len(keyWordArr) < 3 else keyWordArr[2]

	soup = requestAssemblor(searchWord)

	titleAndUrl = [(re.sub(u'<[\d\D]*?>', ' ', str(item)), item['href']) for item in soup.select('div#ires div.g h3 > a')]
	rawSourceAndTime = [re.sub(u'<[\d\D]*?>', ' ', str(item)) for item in soup.select('div#ires div.g div.slp')]
	sourceAndTime = [extractMediaExpireDate(item) for item in rawSourceAndTime]

	zippedData = list(zip(titleAndUrl, sourceAndTime))
	data = [ ((str(t1[0]).strip(),) + 
		(hashlib.md5(str(t1[0]).strip().encode(encoding='utf-8')).hexdigest(),) + 
		(urlFilter(t1[1]),) + t2 + 
		# (time.mktime(datetime.now().timetuple()),)) for (t1, t2) in zippedData]
		# (datetime.now().timestamp(),)) for (t1, t2) in zippedData]
		(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)) for (t1, t2) in zippedData]
	# print(data)
	# crawlerDB = CrawlerDB()
	# news_ID_list = crawlerDB.insertNewsBatch(data)
	# print(news_ID_list)
	# print("=========")
	return data
