from newspaper import Article


#A new article from TOI

url = 'https://news.google.com/rss/articles/CBMiOmh0dHBzOi8vd3d3LmRhaWppd29ybGQuY29tL25ld3MvbmV3c0Rpc3BsYXk_bmV3c0lEPTExMjY2MjHSAQA?oc=5&hl=en-IN&gl=IN&ceid=IN:en'

def get_summary_of_particular_news(url):
    
    final_dict = {}
    toi_article = Article(url, language="en") # en for English

    #To download the article
    toi_article.download()

    #To parse the article
    toi_article.parse()

    #To perform natural language processing ie..nlp
    toi_article.nlp()
    
    #To extract title
    final_dict['Title'] = toi_article.title
  
    #  "Article's image:"
    final_dict['Image'] = toi_article.top_image

    #To extract text Article's Text:
    final_dict['main_text'] = toi_article.text
   
    #To extract summary Article's Summary:
    final_dict['Summary_article'] = toi_article.summary
    final_dict['keywords_article'] = toi_article.keywords


    # Article's publish_date:"
    final_dict['publish_date'] = toi_article.publish_date
    
    return final_dict


r = get_summary_of_particular_news(url)
print(r)


