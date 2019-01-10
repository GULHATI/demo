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
import os
from django.http import HttpResponse
from models import Customer, Supplier, Technologies, RFQ, TempFile
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, 'landingpage.html')


def gologin(request):
    return render(request, 'loginpage.html')


def custsignuppage(request):
    return render(request, "signuppage.html")


def partnersignuppage(request):
    return render(request, "partnersignuppage.html")


def gohome(request):
    return redirect('index')


def partnerlogin(request):
    return render(request, 'partnerloginpage.html')


def customerdashboard(request):
    return render(request,'customerdashboard.html')


def supplierdashboard(request):
    return render(request,'supplierdashboard.html')


def add_technologies(request):
    return render(request,'newtechnologies.html')


def rfq(request):
    technologies = Technologies.objects.all()
    return render(request, 'request_quote.html', {'tech': technologies})


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


from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage


def save_quotes(request):
    user = request.user
    if request.method == 'POST':
        quote_name = request.POST['quotes']
        technologies = request.POST.getlist('technologies')
        myfile1 = request.FILES.getlist('myfile1')

        rfq = RFQ()
        rfq.quotename = quote_name
        rfq.save()
        rfq = RFQ.objects.get(quotename=quote_name)
        for x in technologies:
            y = Technologies.objects.get(name=x)
            rfq.technologies.add(y)
        rfq.save()
        count = 0
        files = []
        rf = RFQ.objects.get(quotename=quote_name)
        for f in myfile1:
            temp = TempFile()
            temp.name = str(quote_name) + "/" + str(count)
            temp.file = f
            temp.save()
            with default_storage.open(os.path.join(BASE_DIR, 'media', 'temp', f.name), 'wb+') as dest:
                for chunk in f.chunks():
                    dest.write(chunk)
            files.append('temp/'+f.name)
            x = TempFile.objects.get(name=temp.name)
            rf.file1.add(x)
            count = count + 1
        rf.save()
        try:
            rfq = RFQ.objects.get(quotename=quote_name)
            myfile2 = request.FILES['myfile2']
            myfile3 = request.FILES['myfile3']
            if myfile2:
                rfq.file2 = myfile2
            if myfile3:
                rfq.file3 = myfile3

            with default_storage.open(os.path.join(BASE_DIR, 'media', 'temp', myfile2.name), 'wb+') as dest:
                for chunk in myfile2.chunks():
                    dest.write(chunk)
            files.append('temp/' + myfile2.name)

            with default_storage.open(os.path.join(BASE_DIR, 'media', 'temp', myfile3.name), 'wb+') as dest:
                for chunk in myfile2.chunks():
                    dest.write(chunk)
            files.append('temp/' + myfile3.name)
            rfq.save()
        except Exception:
            pass
        print(user.email)
        cus = Customer.objects.get(email=user.email)
        rfq = RFQ.objects.get(quotename=quote_name)
        cus.quotes.add(rfq)
        cus.save()
        # Send email to all suppliers
        for x in technologies:
            mail_subject = 'Requesting quotes'
            message = "Please find the attached documents with information regarding the technology " \
                      "requirement.\nShortly when the customer will open a window to start bidiing.\n" \
                      '30mins will be provided to top 3 suppliers to' \
                      'enter the bid.\n Thanks.\n\n.' \
                      'The above quote is requested for the technology: {}'.format(x)
            s = Supplier.objects.all()
            print(files)
            for y in s:
                email = EmailMessage(
                    mail_subject, message, to=[y.email]
                )
                for f in files:
                    email.attach_file(os.path.join(BASE_DIR, 'media', f))
                email.send()
        return HttpResponse("FIle uploaded successfully")


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def view_quotes(request):
    a = RFQ.objects.all().reverse()
    paginator = Paginator(a, 7)
    page = request.GET.get('page')
    try:
        z = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        z = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        z = paginator.page(paginator.num_pages)
    return render(request, 'view_rfq.html', {'a': z})


def supplier_initial_bid(request):
    if request.method == 'POST':
        quote_name = request.POST['quotename']
        quote_name = str(quote_name)
        a = RFQ.objects.all()
        return render(request, 'supplier_initial_bid.html', {'rfq': a, 'quote_name': quote_name})


