import requests
import pandas as pd
from bs4 import BeautifulSoup

# Replace 'your_url_here' with the URL of the web page you want to scrape.
url_india = 'https://www.indiatoday.in/india'
url_law = 'https://www.indiatoday.in/law-today'
url_tamilnadu_news = 'https://www.indiatoday.in/topic/tamil-nadu'




def india_today_news_india(site_url):
    
    dataframe = pd.DataFrame()
    # Send an HTTP GET request and parse the HTML content
    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div element with the class 'story__grid'
    div_element = soup.find('div', class_='story__grid')

    # Get all the <a> tags inside the div element
    if site_url == "https://www.indiatoday.in/topic/tamil-nadu":
        h2_tags = div_element.find_all('h3')
    else:
        h2_tags = div_element.find_all('h2')
    img_tags = div_element.find_all('img')
    p_tags = div_element.find_all('p')

    # Now, 'a_tags' contains all the <a> tags inside the specified <div> element
    title_list = []
    article_link_list = []

    for h2_tag in h2_tags:
        title_list.append(h2_tag.text)
        article_link_list.append("https://www.indiatoday.in" + h2_tag.find('a')['href'])
        
        
    dataframe["title"] = title_list
    dataframe["article_link"] = article_link_list
    

    brief_list = []
    for p_tag in p_tags:
        brief_list.append(p_tag.text)
    dataframe["description"] = brief_list

    image_list = []
    for img_tag in img_tags:
        image_list.append(img_tag['src'])
    dataframe["image"] = image_list
    
    
    return dataframe


dataframe_url_india = india_today_news_india(url_india)
dataframe_url_law = india_today_news_india(url_law)
dataframe_url_tamilnadu_news = india_today_news_india(url_tamilnadu_news)


d = pd.concat([dataframe_url_india,dataframe_url_law,dataframe_url_tamilnadu_news])
d['channel_name'] = [ "indiatoday" for i in range(len(d))]
d.to_csv("india_today_news.csv")






