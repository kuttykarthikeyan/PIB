import pandas as pd

df = pd.read_csv('india_today_news.csv')

keywords = ['politics', 'nations', 'General']

def keyword_searching(input_dataframe,keyword,search_column_name_from_dataframe):
    matches = input_dataframe[input_dataframe[search_column_name_from_dataframe].str.contains(keyword, case=False)]
    return matches

print(keyword_searching(df,'General','description'))
    
    