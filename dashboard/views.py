from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse
from models import Customer,Supplier,Technologies



def index(request):
    return render(request, 'landingpage.html')

def gologin(request):
    return render(request, 'loginpage.html')

def custsignuppage(request):
    return render(request, "signuppage.html")

def partnersignuppage(request):
    return render(request, "partnersignuppage.html")

def gohome(request):
    return  redirect('index')

def partnerlogin(request):
    return render(request, 'partnerloginpage.html')

def customerdashboard(request):
    return render(request,'customerdashboard.html')

def supplierdashboard(request):
    return render(request,'supplierdashboard.html')

def add_technologies(request):
    return render(request,'newtechnologies.html')

def rfq(request):
    return render(request, 'request_quote.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['usern']
        password = request.POST['password']
        type = request.POST['type']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if type == 'customer':
                c = Customer.objects.get(email = username)
                login(request, user)
                #return HttpResponse("Customer")
                return redirect(customerdashboard)
            elif type == 'partner':
                s = Supplier.objects.get(email =username)
                login(request,user)
                #return HttpResponse("Supplier")
                return redirect(supplierdashboard)
            else:
                return HttpResponse("Invalid Credentials")
        else:
            return HttpResponse("INVALID LOGIN DETAILS")

def signup(request):
    if request.method == 'POST':
        user = User()
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        type = request.POST['type']
        address = request.POST['address']
        pan = request.POST['pan']
        tan = request.POST['tan']
        gst = request.POST['gst']
        user.username = email
        user.set_password(password)
        user.email = email
        user.is_active = False
        user.save()
        if type == 'customer':
            cust = Customer()
            cust.name = fname + ' '+ lname
            cust.email = email
            cust.phone = phone
            cust.pan = pan
            cust.tan = tan
            cust.gst = gst
            cust.address = address
            cust.type = 'customer'
            cust.save()
        else:
            cust = Supplier()
            cust.name = fname + ' ' + lname
            cust.email = email
            cust.phone = phone
            cust.pan = pan
            cust.tan = tan
            cust.gst = gst
            cust.address = address
            cust.type = 'partner'
            cust.save()
        print(user.password)
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('Please confirm your email address to complete the registration')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        username = user.username
        try:
            c = Customer.objects.get(email=username)
        except:
            c = None
        if c is not None:
            login(request, user)
            return redirect(customerdashboard)
            #return HttpResponse("Customer")
        try:
            s = Supplier.objects.get(email =username)
        except :
            s = None
        if s is not None:
            login(request, user)
            return redirect(supplierdashboard)
            #return HttpResponse("Supplier")
    else:
        return HttpResponse('Activation link is invalid!')



from django.conf import settings
from django.core.files.storage import FileSystemStorage


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile1 = request.FILES['myfile1']
        myfile2 = request.FILES['myfile2']
        myfile3 = request.FILES['myfile3']
        fs = FileSystemStorage()
        filename = fs.save(myfile1.name, myfile1)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return HttpResponse("FIle uploaded successfully")
