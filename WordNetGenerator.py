#coding=utf-8

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime

def wordNetGenerator(text):
	wordCloud = WordCloud(
        background_color="white", #设置背景为白色，默认为黑色
        width=1500,              #设置图片的宽度
        height=960,              #设置图片的高度
        margin=10               #设置图片的边缘
        ).generate(text)
	# wordcloud = WordCloud().generate(text)
	# plt.imshow(wordCloud, interpolation='bilinear')
	# plt.axis("off")

	# #max_font_size设定生成词云中的文字最大大小
	# #width,height,margin可以设置图片属性
	# # generate 可以对全部文本进行自动分词,但是他对中文支持不好
	# wordcloud = WordCloud(max_font_size=66).generate(text)
	# plt.figure()
	# plt.imshow(wordcloud, interpolation="bilinear")
	# plt.axis("off")
	# plt.show()
	fileName = ("/Users/xiaoyongbo/Documents/projects/hawkeye.v.0.2/report/%s.png" % datetime.now().strftime("%Y-%m-%d"))
	try: 
		wordCloud.to_file(fileName)
	except Exception as e:
		logger.error("wordCloud save file error: %s" % str(e))

	return fileName

# if __name__ == '__main__':
	# WordNetGenerator