from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Book,Profile,SignUp
from .forms import ImageForm,EmailSignUpForm
from django.conf import settings
from django.http import HttpResponseRedirect  
import json
import requests

# Create your views here.
def home(request):
    books = Book.objects.all()
    return render(request,"Turnshop.html",{'books': books})

def login(request):
     if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']

         user = auth.authenticate(username=username,password=password)

         if user is not None:
             auth.login(request,user)
             return redirect('/')
         else:
             messages.info(request,"Invalid username or password.")
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     else:
         return render(request,'login.html')        

def logout(request):
    auth.logout(request)
    return redirect('/') 

def updateInfo(request):
    if request.method == 'POST':
        email = request.POST['em_field']
        username = request.POST['username']
        user = request.user
        form = ImageForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
      
        if user.username == username:
            if user.email == email:
                return redirect('edit')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"This email has already been used by another account.")
                    return redirect('edit')
                else:
                    user.email = email
                    user.save()
                    messages.info(request,"Your account has been updated successfully!")
                    return redirect('edit') 
        
        else: 
            if user.email == email:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"The username already exists.")
                    return redirect('edit')
                else:
                    user.username = username
                    user.save()
                    messages.info(request,"Your account has been updated successfully!") 
                    return redirect('edit')
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"The username already exists")
                    return redirect('edit')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.info(request,"This email has already been used by another account.")
                        return redirect('edit')
                    else:
                        user.username = username
                        user.email = email
                        user.save()   
                        messages.info(request,"Your account has been updated successfully!") 
                        return redirect('edit')     
         

       

def edit(request): 
    return render(request,"updateInfo.html")

MAILCHIMP_API_KEY = settings.MAILCHIMP_API_KEY
MAILCHIMP_DATA_CENTER = settings.MAILCHIMP_DATA_CENTER
MAILCHIMP_EMAIL_AUDIENCE_ID = settings.MAILCHIMP_EMAIL_AUDIENCE_ID

url_api = f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
members_endpoint = f'{url_api}/lists/{MAILCHIMP_EMAIL_AUDIENCE_ID}/members'

def inscribeToAudience(email):
    data = {
        "email_address": email,
        "status": "subscribed", 
    }
    r = requests.post(
        members_endpoint,
        auth=('',MAILCHIMP_API_KEY),
        data=json.dumps(data)
    )
    return r.status_code,r.json()

def subscribe(request):
    email = request.POST['email']
    form = EmailSignUpForm(request.POST) 
    if request.method == 'POST':
        if form.is_valid():
            #check if user has already subscribed to newsletters
            queryset = SignUp.objects.filter(email=email)
            if queryset.exists():
                #messages.info(request,"You have already subscribe to our newsletters")
                pass
            else:
                inscribeToAudience(email)
                form.save()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    