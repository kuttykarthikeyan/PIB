from tqdm import tqdm
from multiprocessing import Pool
from tqdm import tqdm
import pandas as pd
from newspaper import Article
from gnews import GNews
import pandas as pd
from datetime import datetime  
from transformers import pipeline



zero_shot_classifier = pipeline('zero-shot-classification', model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", device=-1)
def sentiment_analysis(descriptions):
    global zero_shot_classifier
    list_results = []
    descriptions = descriptions
    for text in descriptions:
        results = {}
        class_names = ["POSITIVE", "NEUTRAL", "NEGATIVE"]
        answer = zero_shot_classifier(text, class_names, hypothesis_template="The sentiment of this text is {}.")
        answer = answer
        sentiment = answer['labels']
        sentiment_intensity = (answer['scores'])
        results['SENTIMENT_LABEL'] = sentiment[0]
        results[sentiment[0].upper()] = round(abs(sentiment_intensity[0]) * 100,2)
        results[sentiment[1].upper()] = round(abs(sentiment_intensity[1]) * 100,2)
        results[sentiment[2].upper()] = round(abs(sentiment_intensity[2]) * 100,2)
        list_results.append(results)  
    return list_results

def time_age_function(publist_date):
    from datetime import datetime

    # Define the target datetime
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # target_datetime = datetime.strptime(publist_date, date_format)
    target_datetime = publist_date

    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the time difference
    time_difference = current_datetime - target_datetime

    # Extract the time difference components (days, seconds, etc.)
    days = time_difference.days
    seconds = time_difference.seconds

    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Print the time difference
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ago"
    
google_news = GNews()
def get_summary_of_particular_news(url):
    
    global google_news
    
    final_dict = {}
   
    toi_article = google_news.get_full_article(url)
    print(toi_article)
    #  "Article's image:"
    final_dict['image'] = [ i for i in list(toi_article.images) if  i[0:8] == "https://" ][0]
    

    #To extract text Article's Text:
    final_dict['main_text'] = toi_article.text
    

   
    return final_dict

from tqdm import tqdm
import pandas as pd

def time_age_function(publist_date):
    from datetime import datetime

    # Define the target datetime
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # target_datetime = datetime.strptime(publist_date, date_format)
    target_datetime = publist_date

    # Get the current datetime
    current_datetime = datetime.now()

    # Calculate the time difference
    time_difference = current_datetime - target_datetime

    # Extract the time difference components (days, seconds, etc.)
    days = time_difference.days
    seconds = time_difference.seconds

    # Calculate hours, minutes, and remaining seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Print the time difference
    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ago"
    
    
def main_function(prompt,language,max_results,past_no_of_hours):
        
    date_format = "%a, %d %b %Y %H:%M:%S GMT"

    google_news = GNews()
    # google_news.period =  str(past_no_of_hours)+ 'h'  # News from last 7 days
    google_news.max_results = max_results  # number of responses across a keyword
    google_news.country = 'India'  # News from a specific country 
    google_news.language = language  # News in a specific language
    google_news.exclude_websites = ['yahoo.com', 'cnn.com']
    json_resp = google_news.get_news(prompt)
    

    if len(json_resp) != 0:
        d = []
        
        for dis_1 in json_resp:
            
            try:
                particular_url_data = get_summary_of_particular_news(dis_1['url'])
         
                # split_list = particular_url_data['main_text']
                # split_list_analysis = sentiment_analysis(split_list)

                # dict_analysis = { i:j['SENTIMENT_LABEL'] for i,j in zip(split_list,split_list_analysis)}                      
                # particular_url_data['positive_sentence'] = [ i for i,j in dict_analysis.items() if j == 'POSITIVE' ]
                # particular_url_data['neutral_sentence'] = [ i for i,j in dict_analysis.items() if j == 'NEUTRAL' ]
                # particular_url_data['negative_sentence'] = [ i for i,j in dict_analysis.items() if j == 'NEGATIVE' ]
                
                # p = [ i['POSITIVE'] for i in split_list_analysis]
                # particular_url_data['POSITIVE'] = sum(p) / len(p)
                # particular_url_data['NEUTRAL'] = sum([ i['NEUTRAL'] for i in split_list_analysis]) / len([ i['NEUTRAL'] for i in split_list_analysis])
                # particular_url_data['NEGATIVE'] = sum([ i['NEGATIVE'] for i in split_list_analysis]) / len([ i['NEGATIVE'] for i in split_list_analysis])
                # particular_url_data['sentiment_analysis_result'] = max([ i['SENTIMENT_LABEL'] for i in split_list_analysis])
                
            
                dis_1.update(particular_url_data)
                dataframe_dis = pd.DataFrame([dis_1])
                
                
                if dataframe_dis is not None:
                    d.append(dataframe_dis)
                    
            except:
                
                dis_1.update({'image':'none', 'main_text': 'none'})
                dataframe_dis = pd.DataFrame([dis_1])
                
                if dataframe_dis is not None:
                    d.append(dataframe_dis)
                    

        df = pd.concat(d)
        df['publisher'] = [ i['title']  for i in df['publisher']]
        df['published date']  = [ datetime.strptime(i, date_format) for i in df['published date']]
        df["published time ago"] = [ time_age_function(i)  for i in df['published date']]
        df['published date'] = pd.to_datetime(df['published date'])
        df.sort_values('published date',ascending=False)
        df = df.loc[df['main_text'] != "none"]
        
        sentiment_analysis_result = sentiment_analysis(list(df['main_text']))
        print("!!!!!111",sentiment_analysis_result)
        print(len(df))
     
        df['POSITIVE'] = [ i['POSITIVE'] for i in sentiment_analysis_result]
        df['NEUTRAL'] = [ i['NEUTRAL'] for i in sentiment_analysis_result]
        df['NEGATIVE'] = [ i['NEGATIVE'] for i in sentiment_analysis_result]
        df['SENTIMENT_LABEL'] = [ i['SENTIMENT_LABEL']  for i in sentiment_analysis_result]
        
        return df
    
    else:
        return []
 
# keyword = "politics"
# site = ""
# if site != "":
#     site = " site:" + site
# time_ago = 10
# if time_ago != 0:
#     time_ago = " when:" + str(time_ago) + "h"

# prompt =  keyword + site + time_ago
# print(prompt)

# result = main_function(prompt=prompt ,language="Hindi", max_results=3, past_no_of_hours=5)

# print(result.columns)

# result.to_csv("testingggggg.csv")

# print(result)