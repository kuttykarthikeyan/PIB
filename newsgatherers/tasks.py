from celery import shared_task
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib import messages
from tempfile import NamedTemporaryFile
from django.core.files import File


from newsgatherers.scripts.scrap_news_data import collect_data_for_state,news_scarpe_from_gnews_final
from .models import *
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from .scripts.youtube_video_trimming_process import *
from .scripts.scrap_youtube_data import *

from newspaper import Article
import json
from datetime import datetime


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
def scrap_youtube_data(data):
    try:
        data = json.loads(data)
        for youtube_obj in data:
            youtube_data_obj = news_obj.objects.create(title=youtube_obj.title,views=youtube_obj.views,thumbnail=youtube_obj.thumbnail,link=youtube_obj.link,
                                                        published_time_ago=youtube_obj.published_time_ago,duration_of_video=youtube_obj.duration_of_video,
                                                        channel_name=youtube_obj.channel_name,type_of_platform=youtube_obj.type_of_platform,
                                                        source_type='youtube',sentiment_analysis=youtube_obj.sentiment_analysis,summary_json=youtube_obj.summary_json)       
    except Exception as e:
        print("error occured while saving youtube data at task--> "+str(e))
    
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
 
            news_data_obj = news_obj.objects.create(source_choices='website',title=title,description=description,published_date=published_date,url=url,publisher=publisher,published_time_ago=published_time_ago,State=State,Department=Department,POSITIVE=POSITIVE,NEUTRAL=NEUTRAL,NEGATIVE=NEGATIVE,SENTIMENT_ANALYSIS_RESULT=SENTIMENT_ANALYSIS_RESULT)
            news_data_obj.save()

    except Exception as e:
        print("error occured in news scrapping"+str(e))


