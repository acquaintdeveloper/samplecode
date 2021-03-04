from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages,sessions
from django.shortcuts import render,redirect
from .models import *
from django.template.loader import render_to_string
from django.core.mail import send_mail as mail
from django.utils.html import strip_tags
from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Your account is deactivate please contact to administrator.")
                return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/')
    else:
        return render(request, 'login.html')

def new_user_registrion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = make_password(request.POST['password'])  # for password use make_password method.
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if (User.objects.filter(username = username).count()) >= 1: #check a username in already exits in table or not
            messages.error(request, "Username is already exits.")
            return render (request,'registration.html')

        user = User.objects.create(username = username,password = password,first_name = first_name,last_name = last_name)  #Create new user record
        login(request, user)
        return HttpResponseRedirect('home')
    else:
        return render(request,'registration.html')

def log_out_user(request):
    pass

@login_required
def logout(request):
    log_out_user(request)
    return redirect('sign_in')

def home(request):
    makes = Make.objects.all()
    years = Year.objects.all()
    if request.GET.get('make') or request.GET.get('year'):
            make_filter = request.GET.get('make')
            year_filter = request.GET.get('year')
            cars = Car.objects.filter(make__name = make_filter,year__year = year_filter)
    else:
            cars = Car.objects.all()
    return render(request,'home.html',context={'cars':cars,'makes':makes,'years':years})

def add_car(request):
    makes = Make.objects.all()
    years = Year.objects.all()
    if request.method == 'POST':
        seler_name = request.POST['seller_name']
        seler_contact = request.POST['seller_contact']
        car_name = request.POST['car_name']
        car_model = request.POST['car_model']
        year = request.POST['year']
        condition = request.POST['condition']
        amount = request.POST['amount']

        car_obj = Car(seller_name=seler_name,seller_mobile=seler_contact,car_model=car_model,condition=condition,amount=amount)
        car_obj.make_id = car_name
        car_obj.year_id = year
        car_obj.save()
        return redirect('thankyou')
    return render(request,'add_car.html',{'makes':makes,'years':years})

def thankyou(request):
    return render(request, 'thankyou.html')

@transaction.atomic
def send_mail(request,car_id):
    if request.method == 'POST':
        car_data = Car.objects.filter(id = int(car_id)).first()
        html_message = render_to_string('mail_detail.html', {
            'car_data': car_data,
            'intersted_party_name' :request.POST['intersted_party_name'],
            'intersted_party_number' :request.POST['intersted_party_contact']
        })
        car_data.is_buy = True
        mail("Enter your subject", strip_tags(html_message), settings.EMAIL_HOST_USER , ["mike@example.org"], html_message=html_message)
        return HttpResponseRedirect('')
    else:
        return render(request,'mail.html')


def make_available(request,car_id):
    Car.objects.filter(id = car_id).update(is_buy=False)
    return redirect('home')


