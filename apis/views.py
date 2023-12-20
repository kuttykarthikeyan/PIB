from django.shortcuts import render
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from rest_framework.response import Response
from .models import *
import pandas as pd
from rest_framework import status
from newspaper import Article
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views import View
import datetime
from newsgatherers.tasks import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import seaborn as sns
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

from newsgatherers.scripts.youtube_video_trimming_process import sentiment_analysis
from asgiref.sync import sync_to_async
from youtube_transcript_api import YouTubeTranscriptApi
import asyncio

from newsgatherers.models import *
# Create your views here.
from newsgatherers.scripts.urlmapper import *
from newsgatherers.scripts.youtube_video_trimming_process import *


def youtube_video_data_analysis(request):
    
    print('im from youtube_video_data_analysis')
    if request.method == 'POST':    
        
        print(request.POST)
        id = request.POST.get('id')
        
        youtube_video = youtube_data.objects.get(id=id)
        youtube_video_url = youtube_video.link
        youtube_video_data = youtube_video_trimming_process(youtube_video_url)
        json_youtube_csv_content = youtube_video_data.to_json(orient='records')
        youtube_data_list = json.dumps(json_youtube_csv_content)
        
        response_data = {
            'success': True,
            'message': f'Video ID {id} processed successfully',
            'youtube_data_list': youtube_data_list  
        }
        return JsonResponse(response_data, safe=False)
    return JsonResponse({'success': False})

@api_view(['POST'])
def save_youtube_data(request):
    if request.method == "POST":
        try:
            if request.data:
                data = request.data
                scrap_youtube_data.delay(data)
                return JsonResponse({'status': True,'data': 'data recieved'})
            else:
                print('no data recieved')
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': 'no data recieved'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error occured on storing data at api endpoint--->'+str(e))
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'success': True})


@api_view(['POST'])
def scrap_news_clustered_data(request):
     if request.method =="POST":
        try:
                if request.data:
                    data = request.data
                    scrap_news_cluster_data.delay(data)
                    return JsonResponse({'status': True,'data': 'data recieved'})
                else:
                    print('no data recieved')
                    return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': 'no data recieved'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('error occured on storing data at api endpoint--->'+str(e))
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)
     return JsonResponse({'success': True})

@api_view(['GET'])
def get_negative_clips(request,id):
    try:
        url = news_obj.objects.get(id=id).link
        crop_negative_clips = get_negative_videos_task(url,id)
        return JsonResponse({'status': True,'data': crop_negative_clips})
    except Exception as e:
        print(str(e))
        return JsonResponse({'status': False, 'data': 'An error occurred'+str(e)})

def tokenize_and_clean(text):
        words = word_tokenize(str(text).lower())
        stop_words = set(stopwords.words('english'))
        return [word for word in words if word.isalpha() and word not in stop_words]


@api_view(['GET'])
def get_word_cloud(request,id):
    try:
        print(id)
        obj = news_obj.objects.get(id=id)
        sentiment_analysis = obj.sentiment_analysis
        sentiment_analysis = json.loads(sentiment_analysis)
        data_array = []
        for categories in sentiment_analysis:
            data_array.append(categories['subtitle'])
        data = " ".join(data_array)
        print(data)
        
        if not data:
            print("##########")
            return JsonResponse({'status': False, 'data': 'no data recieved'})
        else:
            
            print(data)
        
            # data = json.loads(json)
            nltk.download('vader_lexicon')
            
            
            print("image comedfffffffff wordcloud") 
            
            l = tokenize_and_clean(data)
            all_words = ' '.join(l)
            
            print("image comejjjjjjjjj wordcloud")

            wordcloud = WordCloud(width=800, height=400, max_words=200, background_color='white').generate(all_words)
            print("image come wordcloud")
            wordcloud.to_file("newsgatherers/static/wordcloud_image.png")
            print("image come saved")
            return JsonResponse({'status': True,'data': 'newsgatherers/static/wordcloud_image.png'})

    except Exception as e:
        print("error occured")
        return JsonResponse({'status': False, 'data': 'An error occurred'+str(e)})