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

def signin(request):
    if request.method == 'POST':
        username = request.POST['usern']
        password = request.POST['password']
        type = request.POST['type']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("INVALID LOGIN DETAILS")

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        company = request.POST['company']
        phone = request.POST['phone']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        user = User()
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        company = request.POST['company']
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
        username = user.username
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')
