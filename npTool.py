import newspaper
from newspaper import Article
from NPExtractor import NPExtractor

# target_url = "https://www.google.com.hk/search?q=china&newwindow=1&safe=strict&source=lnms&tbm=nws&sa=X&ved=0ahUKEwjEpcOBg4beAhUrllQKHdjTAIYQ_AUIDygC&biw=1280&bih=698&dpr=2&num=20&tbs=qdr:n60,sbd:1&hl=en"
# target_url = "https://www.google.com.hk/search?q=china&safe=strict&tbm=nws&source=lnt&tbs=qdr:h&sa=X&ved=0ahUKEwjNhfiIs8TgAhUFc3AKHVIdALwQpwUIHg&biw=1280&bih=698&dpr=2"
# cnn_paper = newspaper.build(target_url)

# https://www.google.com.hk/search?q=china&newwindow=1&safe=strict&source=lnms&tbm=nws&sa=X&ved=0ahUKEwjEpcOBg4beAhUrllQKHdjTAIYQ_AUIDygC&biw=1280&bih=698&dpr=2&num=20&tbs=qdr:n60,sbd:1&hl=en

url = 'https://www.channel3000.com/news/politics/national-politics/us-china-trade-talks-resume-as-deadline-looms/1028518268'
 
a = Article(url, language='en') # Chinese
 
a.download()
a.parse()
print(a.authors)
print(a.text)
print("++++++++++++++")
a.nlp()
print(a.keywords)
print("++++++++++++++")
np_extractor = NPExtractor(a.text)
kws_result = np_extractor.extract()
print(kws_result)
print("++++++++++++++")
print(a.summary)
 
# for article in cnn_paper.articles:
#     print(article.url)

# print("===========")
 
# for category in cnn_paper.category_urls():
#     print(category)
 
# article = cnn_paper.articles[0]
# article.download()
 
# article.html
# article.parse()
 
# article.authors
 
# article.text
 
# article.top_image
 
# article.movies
# article.nlp()
 
# article.keywords
 
# article.summary