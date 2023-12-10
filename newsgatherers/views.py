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
from newsgatherers.scripts.urlmapper import *
from .tasks import *
from newsgatherers.scripts.youtube_video_trimming_process import sentiment_analysis
from asgiref.sync import sync_to_async
from youtube_transcript_api import YouTubeTranscriptApi
import asyncio
from .forms import *
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.info(request, "Invalid Username or Password")

    return render(request, 'login.html')

def signup(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        print(request.POST)
        if  password==confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info('The user already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email,first_name=firstname,last_name=lastname,username=email)
                user.set_password(password)
                user.is_staff=True
                user.is_superuser=True
                user.save()
                return redirect('login')
    else:
        print("this is not post method")
        return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('admin_dashboard')

def admin_dashboard(request):
    context = {}
    latest_news = News.objects.all()
    for news in latest_news:
        data = pd.read_csv(news.data, low_memory=False)
        data['id'] = news.id
        data['POSITIVE'] = round(data['POSITIVE']*100,2)
        data['NEGATIVE'] = round(data['NEGATIVE']*100,2)
        data['NEUTRAL'] = round(data['NEUTRAL']*100,2)
 
        
            
    json_data = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_data)
    
    context = {"data":data}

    context = {"data":data,"all_data":latest_news} 

    return render(request,'admin_dashboard.html',context)





def article(request,index,id):
    context={}
    news = News.objects.get(id=id)
    data = pd.read_csv(news.data, low_memory=False)
    json_data = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_data)
    summary = {}
    for article in data:
        if article['index'] == index:
            article_data = article
            
            url = article_data['url']
            summary = get_summary_of_particular_news(url)
            print(summary)
            context={"summary":summary}
            break
    
    return render(request,'article.html',context)

def youtube_data_home(request):
    context={}
    try:
        data = youtube_data.objects.filter(channel_name='indiatoday')
        context = {"data":data}
    except Exception as e:
        print(str(e))
    return render(request,'youtube_home.html',context)

       
def youtube_data_analysis(request,id):
    print(id)
    youtube_video = youtube_data.objects.get(id=id)
    context = {'youtube_data':youtube_video}
    print(context)
    return render(request,'youtube_data_analysis.html',context)

def admin_dashboards(request):
    context = {}
    latest_news = News.objects.all()
    for news in latest_news:
        data = pd.read_csv(news.data, low_memory=False)
        data['id'] = news.id

    json_data = data.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_data)
    
    context = {"data":data}

    context = {"data":data,"all_data":latest_news}

    return render(request,'admin_dashboards.html',context)

def eprints(request):
    forms = Eprintsform()
    if request.method == 'POST':
        print("requws",request.FILES)
        forms = Eprintsform(request.POST,request.FILES)
        print('form',forms)
        if forms.is_valid():
            forms.save()
            return redirect('eprint')
    context={'forms':forms}
    return render(request,'eprints.html',context)

def eprint(request):
    prints = Eprints.objects.all()
    context = {'prints':prints}
    return render(request,'eprint.html',context)


def text_video(request):
    return render(request,'text_video.html')
def newsanalysis(request):
    return render(request,'newsanalysis.html')

def youtubes(request):
    return render(request,'youtubes.html')