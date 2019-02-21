#coding=utf-8

import datetime
import smtplib
import os.path
import mimetypes
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from Logger import logger

def emailContentGenerator(summaryInfo, rowsContent):
	mailMsgContent = """<html><body>""" + summaryInfo + """<table border='1' cellspacing='0'>"""
	mailMsgContent = mailMsgContent + rowsContent
	mailMsgContent += """</table></body></html>"""
	return mailMsgContent

def roundSummaryInfoGenerator(num):
	return """<p>timestamp: """ + datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S') + """</p><p>total news number: """ + str(num) + """</p><br/>"""

def tableRowContentGenerator(title, date, url, keyWords, summary):
	# rowContent = "<td><a href='" + url + "'>" + title + "</a></td><td>" + date + "</td><td>" + keyWords + "</td><td>" + summary + "</td>"
	rowContent = "<tr style='background-color:antiquewhite;text-align:center;'><td><a href='" + url + "'>" + title + "</a></td></tr>"
	rowContent += "<tr style='text-align:center;'><td>" + date + "</td><td>"
	rowContent += "<tr style='text-align:center;'><td>" + keyWords + "</td><td>"
	rowContent += "<tr style='color: darkgray;'><td>" + summary + "</td><td>"
	# return """<tr>""" + rowContent + """</tr>"""
	return rowContent

sender = 'host_to_email@163.com'
pwd = '******'
receivers = ['xiaoyb.shawn@protonmail.com']

def sendMail(subContent, bodyContent):
	server = smtplib.SMTP('smtp.163.com', 25)
	server.login(sender, pwd)

	msg = MIMEText(bodyContent, 'html', 'utf-8')
	msg['From'] = 'host_to_email@163.com <host_to_mail@163.com>'
	msg['Subject'] = Header(subContent, 'utf8').encode()
	msg['To'] = u'Shawn <xiaoyb.shawn@protonmail.com>'
	try:
		server.sendmail(sender, receivers, msg.as_string())
		logger.info("email has been sent...")
	except smtplib.SMTPException:
	    logger.error("email send fail...")

def sendReportMail(subContent, filePath, numberOfNews):
	server = smtplib.SMTP('smtp.163.com', 25)
	server.login(sender, pwd)

	main_msg = MIMEMultipart()
	main_msg['From'] = 'host_to_email@163.com <host_to_mail@163.com>'
	main_msg['To'] = u'Shawn <xiaoyb.shawn@protonmail.com>'
	main_msg['Subject'] = Header(subContent, 'utf8').encode()
	
	msgAlternative = MIMEMultipart('alternative')
	main_msg.attach(msgAlternative)

	mail_msg = """
	<p>Last 24 hours news analysis:</p>
	<p>Total news collected: """ + str(numberOfNews) + """</p><br />
	<p>Key words word-net:</p>
	<p><img src="cid:image1"></p>
	"""
	msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

	try:
		fp = open(filePath, 'rb')
		msgImage = MIMEImage(fp.read())
		fp.close()
	except Exception as e:
		logger.error("email read image file error: %s" % str(e))
		return 
	 
	# 定义图片 ID，在 HTML 文本中引用
	msgImage.add_header('Content-ID', '<image1>')
	main_msg.attach(msgImage)
	 
	try:
	    server.sendmail(sender, receivers, main_msg.as_string())
	    logger.info("email has been sent...")
	except smtplib.SMTPException:
	    logger.error("email send fail...")

if __name__ == '__main__':
	sendReportMail("test", "/Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2/data/Figure_5.png")