from celery import shared_task
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib import messages
from tempfile import NamedTemporaryFile
from django.core.files import File
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
            
            youtube_csv_data.objects.create(title=title,views=views,thumbnail=thumbnail,link=link,published_time_ago=published_time_ago,duration_of_video=duration_of_video,channel_name=channel_name,type_of_platform=type_of_platform)
             
    except Exception as e:
        print(str(e))
    
