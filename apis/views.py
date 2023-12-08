from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import *
import pandas as pd
from newspaper import Article
import json
from django.http import JsonResponse
from django.views import View
import datetime


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
        
        youtube_video = youtube_csv_data.objects.get(id=id)
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
    