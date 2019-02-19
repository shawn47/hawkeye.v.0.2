#coding=utf-8

from datetime import datetime
from datetime import timedelta
import string
import time
import os
import random
import sys

from config import DOMAIN, USER_AGENT, ROOT_FILE

def extractRelativeCountrys(text):
	relativeCountrs = []
	key_word_file = os.path.join(os.path.join(ROOT_FILE, 'data'), 'countrys.csv')
	with open(key_word_file, 'r') as countryList:
		for country in countryList:
			countryNameA = country.split(",")[0]
			if countryNameA in text:
				relativeCountrs.append(countryNameA)
			else:
				for cname in country.split(","):
					if " " + cname + " " in text:
						relativeCountrs.append(countryNameA)

	return relativeCountrs

def urlFilter(rawUrl):
	if "/url?q=" in rawUrl:
		rawUrl = rawUrl.split("/url?q=")[1]
	if "/url?url=" in rawUrl:
		rawUrl = rawUrl.split("/url?url=")[1]
	if "&" in rawUrl:
		rawUrl = rawUrl.split("&")[0]
	if rawUrl[-1:] == '/':
		rawUrl = rawUrl[0:-1]
	return rawUrl

def extractMediaExpireDate(raw):
	now = datetime.today()
	
	mediaInfo = raw.split("-")[0].strip() 
	rawTimeInfo = raw.split("-")[1].strip()
	# timeClapse = ''
	# if "hour" in rawTimeInfo or "小时" in rawTimeInfo:
	# 	timeClapse = timedelta(hours = (24 - int(rawTimeInfo.split(" ")[0])))
	# elif "minute" in rawTimeInfo or "分钟" in rawTimeInfo:
	# 	timeClapse = timedelta(minutes = (24 * 60 - int(rawTimeInfo.split(" ")[0])))
	# else:
	# 	timeClapse = timedelta(minutes = 0)
	# expireDate = now + timeClapse
	
	return (mediaInfo, rawTimeInfo)

def getRandomDomain():
	domain = random.choice(get_data('domains.txt', DOMAIN))
	return domain

def getRandomUserAgent():
	user_agent = random.choice(get_data('user_agents.txt', USER_AGENT))
	return user_agent

def get_data(filename, default = ''):
	domain_files = os.path.join(
	    os.path.join(ROOT_FILE, 'data'), filename)
	try:
	    with open(domain_files) as fp:
	        data = [_.strip() for _ in fp.readlines()]
	except:
	    data = [default]
	return data
