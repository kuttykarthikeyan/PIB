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