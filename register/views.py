from django.shortcuts import render

# Create your views here.

import django.contrib.auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm

from register.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
# Create your views here.

@csrf_exempt
def register_user(request):
    if request.method == 'GET':
        return render(request, 'register/register.html', {'form': RegisterForm()})
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        print(form.is_bound)
        if form.is_valid():
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                ##add user to database as well
                user.save()
                return render(request, 'payapp/home.html', {'success': True})
            except any as e:
                print("error")
                print(e)

        else:
            return render(request, 'payapp/home.html', {'success':False})
    else:
        return HttpResponseRedirect('/errormsg/')

@csrf_exempt
def login_user(request):
    if request.method == 'GET':
        return render(request, 'register/login.html', {'login_form': LoginForm()})
    elif request.method == "POST":
        auth = authenticate(username=request.POST['username'], password=request.POST['password'])
        if auth is not None:
            print("authentic")
            login(request, auth)
            if True: ##user is an admin user
                return render (request, 'payapp/adminHome.html', {'success': True})
            else: ##normal user
                return render(request, 'payapp/home.html', {'success':True, 'user': auth})
        else:
            print("error")
            return render(request, 'payapp/home.html', {'success':False})
    else:
            return render(request, 'payapp/home.html', {'success':"request not valid"})

@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        django.contrib.auth.logout(request)
        return render(request, 'payapp/home.html', {'success':"successfully logged out"})
    else:
        return render(request, 'payapp/home.html', {'success':"tf are you doing"})