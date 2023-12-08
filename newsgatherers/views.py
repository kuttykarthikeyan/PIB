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
        data = youtube_csv_data.objects.filter(channel_name='indiatoday')
        context = {"data":data}
    except Exception as e:
        print(str(e))
    return render(request,'youtube_home.html',context)

# class youtube_data_analysis(View):
    
#     def youtube_video_trimming_process(self,url):
#         indian_languages_interchanged = {"Bangla": "bn", "Bhojpuri": "bho", "Gujarati": "gu", "Hindi": "hi", "Kannada": "kn", "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Odia": "or", "Punjabi": "pa", "Sanskrit": "sa", "Tamil": "ta", "Telugu": "te", "Urdu": "ur"}
#         all_languages = {'Afrikaans': 'af', 'Akan': 'ak', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Assamese': 'as', 'Aymara': 'ay', 'Azerbaijani': 'az', 'Bangla': 'bn', 'Basque': 'eu', 'Belarusian': 'be', 'Bhojpuri': 'bho', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Burmese': 'my', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-Hans', 'Chinese (Traditional)': 'zh-Hant', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Divehi': 'dv', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Ewe': 'ee', 'Filipino': 'fil', 'Finnish': 'fi', 'French': 'fr', 'Galician': 'gl', 'Ganda': 'lg', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Guarani': 'gn', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw', 'Korean': 'ko', 'Krio': 'kri', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lingala': 'ln', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Māori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Nepali': 'ne', 'Northern Sotho': 'nso', 'Norwegian': 'no', 'Nyanja': 'ny', 'Odia': 'or', 'Oromo': 'om', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt', 'Punjabi': 'pa', 'Quechua': 'qu', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Sanskrit': 'sa', 'Scottish Gaelic': 'gd', 'Serbian': 'sr', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Southern Sotho': 'st', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tajik': 'tg', 'Tamil': 'ta', 'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Tigrinya': 'ti', 'Tsonga': 'ts', 'Turkish': 'tr', 'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Western Frisian': 'fy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}

#         video_id = url.split("=")[1]
#         # retrieve the available transcripts
        
#         try:
#             transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    
#             # iterate over all available transcripts
#             for transcript in transcript_list:
#                 # whether it has been manually created or generated by YouTube
#                 transcript.video_id,
#                 detected_lan = transcript.language_code,
#                 # whether this transcript can be translated or not
#                 transcript.is_translatable
                
#                 actual_subtitle = transcript.fetch()   
                
#             subtitle_dict = {}
#             subtitle_dict["subtitle"] = [ i["text"] for i in actual_subtitle]
#             subtitle_dict["start_time"] = [ i["start"]  for i in actual_subtitle]
#             subtitle_dict["end_time"] = [ i["start"] + i["duration"] for i in  actual_subtitle]


#             sentiment_analysis_result = sentiment_analysis(list(subtitle_dict["subtitle"]))    
#             subtitle_dict['POSITIVE'] = [ i['POSITIVE'] for i in sentiment_analysis_result]
#             subtitle_dict['NEUTRAL'] = [ i['NEUTRAL'] for i in sentiment_analysis_result]
#             subtitle_dict['NEGATIVE'] = [ i['NEGATIVE'] for i in sentiment_analysis_result]
#             subtitle_dict['SENTIMENT_ANALYSIS_RESULT'] = [ i['SENTIMENT_LABEL']  for i in sentiment_analysis_result]


#             video_analysis_dataframe = pd.DataFrame(subtitle_dict)
#             print(video_analysis_dataframe)
#             video_analysis_dataframe_neg = video_analysis_dataframe.query('SENTIMENT_ANALYSIS_RESULT == "NEG"')
#             r = video_analysis_dataframe_neg
#             # spliting_negative_clip(url,r)
#             return video_analysis_dataframe_neg
        
#         except Exception as e:
#             print("errorrrrrrrrrrrrrrrrrrr === ",str(e))    
#             print("Subtitles are disabled for this video")

#     async def get(self, request, *args, **kwargs):
#         context={}
#         try:
#             id = self.kwargs.get('id')
#             data = youtube_csv_data.objects.get(id=id)
#             result = await youtube_video_trimming_process(data.link)
#             print(result)
            
#         except Exception as e:
#             print('error from async',str(e))
#         return render(request,'youtube_data_analysis.html')
        
def youtube_data_analysis(request,id):
    print(id)
    youtube_video = youtube_csv_data.objects.get(id=id)
    context = {'youtube_video':youtube_video}
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