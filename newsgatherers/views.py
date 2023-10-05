from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import *
import pandas as pd
from newspaper import Article
import json
import datetime
from newsgatherers.scripts.urlmapper import *
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
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
    return redirect('home')

def admin_dashboard(request):
    context = {}
    latest_news = News.objects.all()
    for news in latest_news:
        data = pd.read_csv(news.data, low_memory=False)

    read_df = data.reset_index()
    df_list = read_df.values.tolist()
    df_list = [ i for i in df_list if int(i[7][0]) < 1 ]
    filter_df = pd.DataFrame(data=df_list,columns=read_df.columns)

    json_data = filter_df.to_json(orient ='records')

    data = []
    data = json.loads(json_data)
    
    context = {"data":data}


   
    # print(data)
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
