#coding=utf-8

import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
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

def sendMail(subContent, bodyContent):
    server = smtplib.SMTP('smtp.163.com', 25)
    server.login('host_to_email@163.com', 'qwer1234')
    msg = MIMEText(bodyContent, 'html', 'utf-8')
    msg['From'] = 'host_to_email@163.com <host_to_mail@163.com>'
    msg['Subject'] = Header(subContent, 'utf8').encode()
    msg['To'] = u'Shawn <xiaoyb.shawn@protonmail.com>'
    server.sendmail('host_to_email@163.com', ['xiaoyb.shawn@protonmail.com'], msg.as_string())
    logger.info("email has been sent...")
