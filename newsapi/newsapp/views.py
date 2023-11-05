from django.shortcuts import render,redirect
import requests
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .captcha import FormWithCaptcha

API_KEY = '4a9fe000084b42579b6d0779de15f7d1'


# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login/')
def news(request):

    country = request.GET.get('country')
    category = request.GET.get('category')
    if not country and not category:
        country = 'in'
    if country:
        url = f'https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
    else:
        url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={API_KEY}'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']



    context = {
        'articles' : articles
    }

    return render(request, 'home_new.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if not user.exists():
            messages.warning(request, "Invalid Username")
            return redirect('/login/')
        user = authenticate(username = username, password = password)
        if user is None:
            messages.warning(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/news/')



    return render(request, 'login.html')



def register_page(request):
    context =  {
        'captcha' : FormWithCaptcha,
    }
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.warning(request, "User Name already exists!! Try another")
            return redirect('/register/')


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username =  username
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully")
        return redirect('/login/')

    return render(request, 'register.html', context=context)

def logout_page(request):
    logout(request)
    return redirect('/login/')

