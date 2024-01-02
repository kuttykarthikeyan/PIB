import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the XML file
xml_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"

# Fetch the XML content from the URL
response = requests.get(xml_url)
xml_content = response.content

# Parse the XML content with BeautifulSoup
soup = BeautifulSoup(xml_content, 'xml')  # Use 'xml' parser for RSS feeds

# Extract information from each item
data = []
for item in soup.find_all('item'):
    title = item.find('title').text
    approx_traffic = item.find('ht:approx_traffic').text
    description = item.find('description').text
    link = item.find('link').text
    pub_date = item.find('pubDate').text
    picture = item.find('ht:picture').text
    picture_source = item.find('ht:picture_source').text

    news_items = []
    for news_item in item.find_all('ht:news_item'):
        news_item_title = news_item.find('ht:news_item_title').text
        news_item_snippet = news_item.find('ht:news_item_snippet').text
        news_item_url = news_item.find('ht:news_item_url').text
        news_item_source = news_item.find('ht:news_item_source').text

        news_items.append({
            "title": news_item_title,
            "snippet": news_item_snippet,
            "url": news_item_url,
            "source": news_item_source
        })

    item_data = {
        "title": title,
        "approx_traffic": approx_traffic,
        "description": description,
        "link": link,
        "pub_date": pub_date,
        "picture": picture,
        "picture_source": picture_source,
        "news_items": news_items
    }

    data.append(item_data)


df = pd.DataFrame(data)
df.to_csv("xxx.csv")

# Display the DataFrame
print(df)
