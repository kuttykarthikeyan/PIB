from newsapi import NewsApiClient
import pandas as pd

api = NewsApiClient(api_key='5d92a84bce57421a8273a7172a2c8e6d')

result = api.get_everything(sources="bbc-news",page_size=100)

dataframe_list = []
for data in result['articles']:
    dataframe_list.append(pd.DataFrame(data=[data]))
    
final_df = pd.concat(dataframe_list)

final_df.to_csv("NewsApiClient_api_news.csv")
    
