from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        n_password = request.POST['n_password']
        c_password = request.POST['c_password']
        
        if n_password == c_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"The username already exists")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.warning(request,"This email has already been used by another account")
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=n_password,email=email)
                    user.save()    
                    return redirect('register')            
        else:
            messages.warning(request,"The passwords entered do not match")
            return redirect('register')

    else:
        return render(request,'Register.html') 