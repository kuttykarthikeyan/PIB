import requests
import pandas as pd
from bs4 import BeautifulSoup

# Replace 'your_url_here' with the URL of the web page you want to scrape.
url_polities = 'https://economictimes.indiatimes.com/news/politics'


def economictimes_news_scrape_polities(site_url):
    
    dataframe = pd.DataFrame()
    # Send an HTTP GET request and parse the HTML content
    response = requests.get(site_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div element with the class 'story__grid'
    div_element = soup.find('section', id='bottomPL')


    # Get all the <a> tags inside the div element
 
    h2_tags = div_element.find_all('h3')
    p_tags = div_element.find_all('p')
    img_tags = div_element.find_all('img')
    published_date_tags = div_element.find_all('time')

    # Now, 'a_tags' contains all the <a> tags inside the specified <div> element
    title_list = []
    article_link_list = []

    for h2_tag in h2_tags:
        title_list.append(h2_tag.text)
        article_link_list.append("https://economictimes.indiatimes.com/" + h2_tag.find('a')['href'])
        
        
    dataframe["title"] = title_list
    dataframe["article_link"] = article_link_list
    
    brief_list = []
    for p_tag in p_tags:
        brief_list.append(p_tag.text)
    dataframe["description"] = brief_list

    image_list = []
    published_time_list = []
    
    for img_tag,time_tag in zip(img_tags,published_date_tags):
        image_list.append(img_tag['src'])
        published_time_list.append(time_tag.text)
        
    dataframe["image"] = image_list
    dataframe["published_time"] = published_time_list
    
    return dataframe

d= economictimes_news_scrape_polities(url_polities)
d['channel_name'] = [ "economictimes" for i in range(len(d))]

d.to_csv("economictimes_news_polities.csv")