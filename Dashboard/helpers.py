from django.core.mail import send_mail
# for generating the random token or string
from datetime import datetime
from django.conf import settings
import os

host_url = os.environ.get('HOST_URL')


def send_forget_password_mail(email,token,uid):
    subject = "Forgot Password Link"
    message = f"Hi click here to change your password {host_url}/resetPassword/{uid}/{token}/"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
    return True
def send_email_verification(email,token,uid):
    try:
        subject = "Your account needs to be verified "
        message = f"click on the link to verify {host_url}/verify/{uid}/{token}/"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject,message,email_from,recipient_list)
    except:
        return False    
    return True
def createRequestBodyForCC(request):
    features = request.POST["transactionsDetails"]
    features  = features.split()
    body={}
    try:
        date = features[1]
        time = features[2]
        custom_id= int(features[0])
        custom_x = float(features[3])
        custom_y=  float(features[4])
        term_x =  float(features[5])
        term_y =  float(features[6])
        amount=   float(features[7])
        dis = ((abs(custom_x-term_x))**2+(abs(custom_y-term_y))**2)**.5
        print(dis)
        format_string = "%Y-%m-%d %H:%M:%S"
        datetime_object = datetime.strptime(date+" "+time, format_string)
        epochTime = datetime_object.timestamp()
       
        body = {'time':epochTime,'dist':dis,'custom_id':custom_id,'amount':amount}
    except Exception as e:
        print(e)
        return "Invalid format"
    return body

    
    



    
    
    
    # {"feature1":request.POST["feature1"],
    #             "feature2":request.POST["feature2"],
    #             "feature3":request.POST["feature3"],
    #             "feature4":request.POST["feature4"],
    #             "feature5":request.POST["feature5"],
    #             "feature6":request.POST["feature6"],
    #             "feature7":request.POST["feature7"],
    #             "feature8":request.POST["feature8"],
    #             "feature9":request.POST["feature9"],
    #             "feature10":request.POST["feature10"],
    #             "feature11":request.POST["feature11"],
    #             "feature12":request.POST["feature12"],
    #             "feature13":request.POST["feature13"],
    #             "feature14":request.POST["feature14"],
    #             "feature15":request.POST["feature15"],
    #             "feature16":request.POST["feature16"],
    #             "feature17":request.POST["feature17"],
    #             "feature18":request.POST["feature18"],
    #             "feature19":request.POST["feature19"],
    #             "feature20":request.POST["feature20"],
    #             "feature21":request.POST["feature21"],
    #             "feature22":request.POST["feature22"],
    #             "feature23":request.POST["feature23"],
    #             "feature24":request.POST["feature24"],
    #             "feature25":request.POST["feature25"],
    #             "feature26":request.POST["feature26"],
    #             "feature27":request.POST["feature27"],
    #             "feature28":request.POST["feature28"],
    #             "feature29":request.POST["feature29"]
                
    #             }
    return requetBody

