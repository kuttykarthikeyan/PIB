from celery import shared_task
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.contrib import messages
import requests
from tempfile import NamedTemporaryFile
from django.core.files import File
from .scripts.optimized_states_wise import *
from apis.serializers import *



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
from .create import *

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
                    source_type=news_obj.youtube,
                    sentiment_analysis=youtube_obj.get('sentiment_analysis', ''),
                    summary_json=youtube_obj.get('summary_json', ''))
            youtube_data_obj.source_type = news_obj.youtube 
            youtube_data_obj.save()      
            print('youtube data created')
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
 
            news_data_obj = news_obj.objects.create(source_choices=news_obj.website,title=title,description=description,published_date=published_date,url=url,publisher=publisher,published_time_ago=published_time_ago,State=State,Department=Department,POSITIVE=POSITIVE,NEUTRAL=NEUTRAL,NEGATIVE=NEGATIVE,SENTIMENT_ANALYSIS_RESULT=SENTIMENT_ANALYSIS_RESULT)
            news_data_obj.save()

    except Exception as e:
        print("error occured in news scrapping"+str(e))

@shared_task
def scrap_news_cluster_data(data):
    try:
        print("creating headdddd")
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
        print(news_head_id,'created headdddddddddddddddd')
        for web_obj in web_cluster:
            print('creating web objjjjjjjj')
            web_object = news_obj()
            for key, value in web_obj.items():
                setattr(web_object, key, value)
            web_object.save()
            obj = news_obj.objects.get(id=web_object.id)
            print(obj)
            obj.source_type=news_obj.website
            obj.clustered = True
            obj.save()
            print('web obj created')
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
            print(obj)
            obj.source_type=news_obj.youtube
            obj.clustered = True
            obj.save()
            news_head = news_cluster_head.objects.get(id=news_head_id)
            news_head.youtube_data_cluster_obj.add(obj)       
            news_head.save()
            print("youtube cluster data saved successfully")
        print("news cluster data saved successfully")
        
    except Exception as e:
        traceback.print_exc()
        print("error occured in news cluster data storing -->"+str(e))



@shared_task
def get_negative_videos_task(url,obj_id):
    
    video_locations = spliting_negative_clip(url,obj_id)
    print(video_locations)
    return video_locations

@shared_task
def scrap_websites_with_clusters_post():

    try:
        # data_frame = scrap_cluster_news()
        data_frame = pd.read_csv(r"D:\PIB\final_data_new.csv")
        data_frame = data_frame.loc[data_frame["main_text"] != "none"]
        print(data_frame)
        data_frame.to_csv("final_data.csv")
        print('data recievedddddddddddddddddddddddddddddd')
        try:
            for index, row in data_frame.iterrows():
                print('data loooooooooooooooopeddddddddddd')
                print(type(data_frame))
                row_dict = row.to_dict()
                data = json.dumps(row_dict)
                try:
                    # post_url = 'http://127.0.0.1:8000/scrap_news_clustered_data/'  
                    # response = requests.post(post_url, data=data, headers={'Content-Type': 'application/json'})
                
                    # if response.status_code == 200:
                    #     print('Data successfully posted to the URL')
                    # else:
                    #     print(f'Error posting data. Status code: {response.status_code}, Response content: {response.text}')
                                
                    
                    # return HttpResponse({'data': data})
                    if data:
                        scrap_news_cluster_data_create(data)
                    else:
                        print('no dataaa')
                except Exception as e:
                    print('error in posting youtube data to endpoint -->'+str(e))

        except Exception as e:
            print('error occured while posting clustered news obj'+str(e))
       
    except Exception as e:
        print('error while scrapping clusters from news-->'+str(e))

@shared_task
def scrap_youtube_videos_instant():
    try:
        youtube_csv_content = scrap_data_from_youtube()
        json_youtube_csv_content = youtube_csv_content.to_json(orient='records')
        youtube_data_list = json.loads(json_youtube_csv_content)
        dataArray = []
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
                if not youtube_video_data:
                    print('no subtitle to analyse')    
                else:
                    summary_json = youtube_video_data.loc[:,['subtitle','SENTIMENT_ANALYSIS_RESULT']].to_json()
                    youtube_data_list = youtube_video_data.to_json(orient='records')
                    if youtube_data_list:
                        
                        youtube_data_obj = news_obj.objects.create(title=title,views=views,thumbnail=thumbnail,link=link,
                                                            published_time_ago=published_time_ago,duration_of_video=duration_of_video,
                                                            channel_name=channel_name,type_of_platform=type_of_platform)
                        youtube_data_obj.sentiment_analysis = youtube_data_list
                        youtube_data_obj.summary_json= summary_json
                        youtube_data_obj.source_type= news_obj.youtube
                        youtube_data_obj.save()
                        print('obj saved --> youtube objsss')
            except Exception as e:
                print("error occured while analysing video -->"+str(e))   
        # for i in dataArray:
        #     print(i)
        # print(type(dataArray))
        # print(len(dataArray))         
        # data = json.dumps(dataArray)
        # print('sucesssssssssssssssssssssssssssssssss')
        # print(data)
        # try:
        #     post_url = 'http://10.1.75.142:8000/save_youtube_data/'  
        #     response = requests.post(post_url, data=data, headers={'Content-Type': 'application/json'})
           
        #     if response.status_code == 200:
        #         print('Data successfully posted to the URL')
        #     else:
        #         print(f'Error posting data. Status code: {response.status_code}, Response content: {response.text}')
                          
        #     return HttpResponse({'data': data})
    except Exception as e:
        print('error in posting youtube data to endpoint -->'+str(e))
            
            
    except Exception as e:
        print("error occured while scraping youtube data --> "+str(e))


@shared_task
def add_recent_neg():
    try:
        data_frame = pd.read_csv(r"D:\PIB\New_Report.csv")
        print(type(data_frame)) 
        
        jsonARR = []
        for index, row in data_frame.iterrows():
                
                publisher = row['publisher']
                NEGATIVE = row['NEGATIVE']
                published_date = row['published_date']
                state = row['state']
                
        negative_publisher_today.objects.create(publisher=publisher,
                                                published_date=published_date,
                                                NEGATIVE=NEGATIVE,state=state)       
        
    except Exception as e:
        print(str(e))

