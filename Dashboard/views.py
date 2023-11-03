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
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .helpers import send_forget_password_mail,createRequestBodyForCC,send_email_verification,fetchAllData
import uuid
from django.core.mail import send_mail
import requests as rq
import uuid
import os

# Create your views here.
def dashboard(request):
     if request.user.is_authenticated:
        res = fetchAllData()
        fraudCount = res[0]
        nonFraudCount = res[1]
        request.session['fraudCount']=fraudCount
        request.session['nonFraudCount']= nonFraudCount
        #context = {'fraudVal': fraudVal, 'nonFraudVal':nonFraudVal}
        return render(request, 'dashboard/index.html')
     messages.error(request,"Please login first")
     return redirect("/")
def verificationSent(request):
   
    display = 'You have registerd successfully'
    if request.session.has_key('login') and request.session['login']=='login':
        display = 'Please verify your email first'
    return render(request,'dashboard/verificationSent.html',{'displayMessage':display})
def verifyEmail(request,token,uidb64):
    try:
       uid = force_str(urlsafe_base64_decode(uidb64))
       user = User.objects.get(pk=uid)
       profile = UsersTable.objects.get(email_token=token)
       print(profile.isVerified)
       user.save()
       profile.isVerified=True
       profile.save()
       loginn(request, user)
    except:
        messages.error(request,"Invalid Token")
        return redirect('/')
    return  redirect('/dashboard')
def login(request):
     if request.method == "POST":
         email = request.POST["email"]
         password = request.POST["password"]
         print(email)
         print(password)
         user =authenticate(request,username=email,password=password)
         if user is not None:
             profile = UsersTable.objects.get(user_id=user.id)
             if profile.isVerified ==False:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    tokens =  str(uuid.uuid4())
                    send_email_verification(email,tokens,uid)
                    profile.email_token = tokens
                    profile.save()
                    request.session['login']='login' 
                    return redirect('/verificationSent')
             subject = "Login Alert"
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
         uid = urlsafe_base64_encode(force_bytes(authobj.pk))
         tokens =  str(uuid.uuid4())
         userTable= UsersTable.objects.create(
             user = authobj,
             email_token = tokens
         )
         send_email_verification(email,tokens,uid)
         userTable.save()
        
         return redirect('/verificationSent')

     return render(request, 'dashboard/register.html')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST["email"]
        user =  User.objects.get(username=email)
        if user is not None:
            token = str(uuid.uuid4())
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            send_forget_password_mail(email,token,uid)
            profile =  UsersTable.objects.get(user_id = user.id)
            profile.forgot_password_token = token
            profile.save()
            messages.success(request, "Please chek Your Email to reset password")
            return redirect('/forgotPassword')
        else:
            return render(request,"dashboard/forgot-password.html",{'error_message':'Email does not exist'})
        
    return render(request,"dashboard/forgot-password.html")


def signout(request):
    logout(request)
    messages.success(request, "You logged out successfully!")
    return redirect("/")
def setPassword(request,):
    if request.method == "POST":
        try:
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']
            if password!=confirmPassword:
                error = {'error_message':'password and confirm password does not match'}
                return  render(request,'dashboard/reset-password.html',error)
            email = request.session['email']
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()
            messages.success(request,"Password changed!")
            return redirect('/')
        except:
              error = {'error_message':'Unexpected Happen!'}
              return  render(request,'dashboard/reset-password.html',error)
def resetPassword(request,token,uidb64):
    if request.method == "POST":
        try:
            password = request.POST['password']
            confirmPassword = request.POST['confirmPassword']
            if password!=confirmPassword:
                error = {'error_message':'password and confirm password does not match'}
                return  render(request,'dashboard/reset-password.html',error)
            email = request.session['email']
            user = User.objects.get(username=email)
            user.set_password(password)
            user.save()
            messages.success(request,"Password changed!")
            return redirect('/')
        except:
              error = {'error_message':'Unexpected Happen!'}
              return  render(request,'dashboard/reset-password.html',error)

    try:
       uid = force_str(urlsafe_base64_decode(uidb64))
       user = User.objects.get(pk=uid)
       profile = UsersTable.objects.get(forgot_password_token=token)
       if profile is not None and profile.user_id==user.id:
           request.session['email']=user.username
           return render(request,'dashboard/reset-password.html')
    except:
        messages.error(request,"Invalid Token")
        return redirect('/')
    return render(request,'dashboard/index.html')
def prediction(request):
    if request.user.is_authenticated:
        request.session['show']=False
        if request.method == "POST":
            requestBody = createRequestBodyForCC(request)
            print(requestBody)
            if requestBody!="Invalid format" :
                base_url = os.environ.get('API_URL')
                response =  rq.post(base_url+'/predictCreditCardFraud',json=requestBody)
                #print(response)
                response = response.json()
                result = response['result']
                print(response)
                request.session['fraudScore']= response['fraud_score']
                request.session['show']=True
                # if result=="Fraudulent":
                #     messages.error(request,result)
                # else:
                #     messages.success(request, result)
                return render(request, 'dashboard/predict.html') 
            else:
                messages.error(request, requestBody)
                return render(request, 'dashboard/predict.html',) 
        return render(request, 'dashboard/predict.html')   
    messages.error(request,"Please login first")
    return redirect("/")


