from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginn
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from .models import UsersTable
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .helpers import send_forget_password_mail,createRequestBodyForCC
import uuid
from django.core.mail import send_mail
import requests as rq

# Create your views here.
def dashboard(request):
     if request.user.is_authenticated:
        return render(request, 'dashboard/index.html')
     messages.error(request,"Please login first")
     return redirect("/")


def login(request):
     if request.method == "POST":
         email = request.POST["email"]
         password = request.POST["password"]
         print(email)
         print(password)
         user =authenticate(request,username=email,password=password)
         if user is not None:
             print(user)
             subject = "Login alert"
             user_ip = request.META.get('REMOTE_ADDR')
             user_browser = request.META.get('HTTP_USER_AGENT')
             from_email = 'iitp2203@gmail.com'
             message = f'hi {user.first_name}, you have loged in from {user_browser} browser and {user_ip} ip address '
             recipient_list=[email]
             send_mail(subject, message, from_email, recipient_list)
             loginn(request,user)
             return  redirect('/dashboard')
         else:
            messages.error(request,"Invalid Credentials!")
            return redirect('/')
             
     return render(request,'dashboard/login.html')
def registration(request):
     if request.method == "POST":
         firstName = request.POST["firstName"]
         lastName = request.POST["lastName"]
         email = request.POST["email"]
         password = request.POST["password"]
         confirmPassword = request.POST["confirmPassword"]
         if User.objects.filter(username=email).first():
             error_message = "Email already exist"
             context = {'error_message': error_message}
             return render(request, 'dashboard/register.html',context)
         if password!=confirmPassword:
             error_message = "password and confirm password does not match"
             context = {'error_message': error_message}
             return render(request, 'dashboard/register.html',context)
         #myuser = User(email=email,firstName=firstName,lastName=lastName,password=hashed_password)
         authobj = User.objects.create_user(username=email, email=email, password=password,first_name = firstName, last_name=lastName)
         authobj.save()
         messages.success(request,"Your account has been successfully created!")
         return redirect("/")
     return render(request, 'dashboard/register.html')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        if User.objects.filter(username=email).first():
            token = str(uuid.uuid4())
            send_forget_password_mail(email,token)
            messages.success(request, "Please chek Your Email!")
            redirect('/forgotPassword')
        else:
            return render(request,"dashboard/forgot-password.html",{'error_message':'Email does not exist'})
        
    return render(request,"dashboard/forgot-password.html")


def signout(request):
    logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("/")
def resetPassword(request):
    return render(request,'dashboard/reset-password.html')
def prediction(request):
    if request.method == "POST":
        requestBody = createRequestBodyForCC(request)
        print(requestBody)
        if requestBody!="Invalid format" :
            base_url = 'http://127.0.0.1:5000'
            response =  rq.post(base_url+'/predictCreditCardFraud',json=requestBody)
            print(response)
            response = response.json()
            result = response['result']
            messages.success(request, result)
            return render(request, 'dashboard/predict.html') 
        else:
            messages.error(request, requestBody)
            return render(request, 'dashboard/predict.html',) 
        

    return render(request, 'dashboard/predict.html')    

