from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        print(request.POST)

        email= request.POST['email']
        password = request.POST['password']
        # user = auth.authenticate(email=email,password=password)

        # if user is not None:
        #     auth.login(request,user)
        #     return redirect('home')
        # else:
        #     messages.info(request,"Inavlid Username or Password")
        #     return redirect('login')
    
    return render(request,'login.html')

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
                user.save()
                return redirect('login')
        else:
            print("this is not post method")
    return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('home')