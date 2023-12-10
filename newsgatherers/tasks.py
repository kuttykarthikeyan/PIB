from celery import shared_task
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib import messages
from tempfile import NamedTemporaryFile
from django.core.files import File

from newsgatherers.scripts.scrap_news_data import collect_data_for_state
from .models import *
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from .scripts.youtube_video_trimming_process import *
from .scripts.scrap_youtube_data import *

from newspaper import Article
import json
import datetime


@shared_task
def render_latest_news(id):
    try:
        news_object = News.objects.get(id=id) 
        print(news_object)
        data = pd.read_csv(news_object.data, low_memory=False)
        data['id'] = news_object.id
        data['POSITIVE'] = round(data['POSITIVE']*100,2)
        data['NEGATIVE'] = round(data['NEGATIVE']*100,2)
        data['NEUTRAL'] = round(data['NEUTRAL']*100,2)       
        json_data = data.reset_index().to_json(orient ='records')
        data = []
        data = json.loads(json_data)
        html_content = render_to_string('admin_dashboard.html', {'context': data})
    except Exception as e:
       print(str(e))

@shared_task
def scrap_youtube_data():
    try:
        youtube_csv_content = scrap_data_from_youtube()
        json_youtube_csv_content = youtube_csv_content.to_json(orient='records')
        youtube_data_list = json.loads(json_youtube_csv_content)
        for content in youtube_data_list:
            title = content["title"]
            views = content["views"]
            thumbnail = content["thumbnail"]
            link = content["link"]
            published_time_ago = content["published_time_ago"]
            duration_of_video = content["duration_of_video"]
            channel_name = content["channel_name"]
            type_of_platform = content["type_of_platform"]
            try:
                youtube_video_data = youtube_video_trimming_process(link)
                summary_json = youtube_video_data.loc[:,['subtitle','SENTIMENT_ANALYSIS_RESULT']].to_json()
                youtube_data_list = youtube_video_data.to_json(orient='records')
                print(youtube_data_list)
                print(summary_json)
                # youtube_data_list = json.dumps(youtube_video_data)
                youtube_data_obj = youtube_data.objects.create(title=title,views=views,thumbnail=thumbnail,link=link,
                                                            published_time_ago=published_time_ago,duration_of_video=duration_of_video,
                                                            channel_name=channel_name,type_of_platform=type_of_platform)
                if youtube_data_list:
                    print('hi im analysed list')
                    youtube_data_obj.sentiment_analysis = youtube_data_list
                    youtube_data_obj.summary_json=summary_json
                    youtube_data_obj.save()
            except Exception as e:
                print("error occured while analysing video -->"+str(e))
    except Exception as e:
        print("error occured while scraping youtube data --> "+str(e))
    
@shared_task
def scrap_news_data():
    try:
        news_csv_content = collect_data_for_state()
        print(type(news_csv_content))

        for news in news_csv_content:
            print(news)
        
        # json_news_csv_content = news_csv_content.to_json(orient='records')
        # news_data_list = json.loads(json_news_csv_content)
        news_data_list = json.dumps(news_csv_content)
        for cont in news_data_list:
    
            title = cont["title"]
            description = cont["description"]
            published_date = cont["published_date"]
            url = cont["url"]
            publisher = cont["publisher"]
            published_time_ago = cont["published_time_ago"]
            State = cont["State"]
            Department = cont["Department"]
            POSITIVE = cont["POSITIVE"]
            NEUTRAL = cont["NEUTRAL"]
            NEGATIVE = cont["NEGATIVE"]
            SENTIMENT_ANALYSIS_RESULT = cont["SENTIMENT_ANALYSIS_RESULT"]
 
            news_data_obj = News.objects.create(title=title,description=description,published_date=published_date,url=url,publisher=publisher,published_time_ago=published_time_ago,State=State,Department=Department,POSITIVE=POSITIVE,NEUTRAL=NEUTRAL,NEGATIVE=NEGATIVE,SENTIMENT_ANALYSIS_RESULT=SENTIMENT_ANALYSIS_RESULT)
            news_data_obj.save()

    except Exception as e:
        print("error occured in news scrapping"+str(e))


