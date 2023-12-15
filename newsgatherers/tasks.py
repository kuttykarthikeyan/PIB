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
import traceback
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
        print(type(data))
        
        for youtube_obj in data:
            youtube_data_obj = news_obj.objects.create(title=youtube_obj.get('title', ''),
                    views=youtube_obj.get('views', 0),
                    thumbnail=youtube_obj.get('thumbnail', ''),
                    link=youtube_obj.get('link', ''),
                    published_time_ago=youtube_obj.get('published_time_ago', ''),
                    duration_of_video=youtube_obj.get('duration_of_video', ''),
                    channel_name=youtube_obj.get('channel_name', ''),
                    type_of_platform=youtube_obj.get('type_of_platform', ''),
                    source_type='youtube',
                    sentiment_analysis=youtube_obj.get('sentiment_analysis', ''),
                    summary_json=youtube_obj.get('summary_json', ''))       
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

@shared_task
def scrap_news_cluster_data(data):
    try:
        
        
        news_cluster_head_obj = news_cluster_head()
        for key in data:
            setattr(news_cluster_head_obj, key, data[key])
            if key == 'website_data_clustering':
                web_cluster = json.loads(data[key])
            if key == 'youtube_data_clustering':
                youtube_cluster = json.loads(data[key])
        print(news_cluster_head_obj.id,"news cluster head idddddddddddddddddddddddddddddddddddddd")
        news_cluster_head_obj.save()
        news_head_id = news_cluster_head_obj.id

        for web_obj in web_cluster:
            web_object = news_obj()
            for key, value in web_obj.items():
                setattr(web_object, key, value)
            web_object.save()
            obj = news_obj.objects.get(id=web_object.id)
            obj.source_type='website'
            news_head = news_cluster_head.objects.get(id=news_head_id)
            news_head.website_data_cluster_obj.add(obj)
            news_head.save()
            print("website cluster data saved successfully")

        for youtube_obj in youtube_cluster:
            youtube_object = news_obj()

            for key, value in youtube_obj.items():
                setattr(youtube_object, key, value)
                
            youtube_object.save()
            obj = news_obj.objects.get(id=youtube_object.id)
            obj.source_type='youtube'
            news_head = news_cluster_head.objects.get(id=news_head_id)
            news_head.youtube_data_cluster_obj.add(obj)       
            news_head.save()
            print("youtube cluster data saved successfully")
        print("news cluster data saved successfully")
        
    except Exception as e:
        traceback.print_exc()
        print("error occured in news cluster data storing -->"+str(e))

        #     youtube_obj = news_obj.objects.create(title=youtube_obj.get('youtube_title', ''),description=youtube_obj.get('youtube_description', '')
        #                                         ,published_date=youtube_obj.get('youtube_published_date', ''),
        #                                     url=youtube_obj.get('youtube_url', ''),source_name=youtube_obj.get('youtube_publisher', '')
        #                                     ,published_time_ago=youtube_obj.get('youtube_published_time_ago', ''),source_type='youtube')
        #     youtube_obj.save()
                # news_cluster_head_obj.youtube_data_cluster_obj.add(youtube_object)
            # web_obj = news_obj.objects.create(title=web_obj.get('title', ''),description=web_obj.get('description', '')
            #                                   ,published_date=web_obj.get('published_date', ''),
            #                                 url=web_obj.get('url', ''),image = web_obj.get('Image', ''),source_name=web_obj.get('publisher', ''),
            #                                 main_text=web_obj.get('main_text', ''),
            #                                 summary_article=web_obj.get("Summary_article",""),
            #                                 positive_sentence=web_obj.get('positive_sentence', ''),neutral_sentence=web_obj.get('neutral_sentence', ''),
            #                                 negative_sentence=web_obj.get('negative_sentence', ''),published_time_ago=web_obj.get('published_time_ago', ''),
            #                                 source_type='website')