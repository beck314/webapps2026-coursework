from django.db import transaction, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.

import django.contrib.auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.forms import AuthenticationForm

from adminPages.models import AdminUsers
from payapp.models import Balance
from register.forms import RegisterForm, InfoForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from register.models import User_Info


# Create your views here.

@csrf_protect
def register_user(request):
    if request.method == 'GET':
        return render(request, 'register/register.html', {'reg_form': RegisterForm(), 'info_form': InfoForm()})
    elif request.method == "POST":
        reg_form = RegisterForm(request.POST)
        info_form = InfoForm(request.POST)
        print(reg_form.is_bound)
        if reg_form.is_valid() and info_form.is_valid() and reg_form.cleaned_data['password1'] == reg_form.cleaned_data['password2']:
            try:
                with transaction.atomic():
                    ##add user to database as well
                    user = reg_form.save()

                    balance = Balance(user=user)
                    balance.save()

                    info_user = user.profile_name
                    info_user.first_name = info_form.cleaned_data.get('first_name')
                    info_user.last_name = info_form.cleaned_data.get('last_name')
                    info_user.phone = info_form.cleaned_data.get('phone')
                    info_user.save()

                    return render(request, 'payapp/home.html', {'success': True})
            except (DatabaseError, ObjectDoesNotExist) as e:
                print("error")
                print(e)

        else:
            return render(request, 'register/register.html', {'success':False})
    else:
        return HttpResponseRedirect('/errormsg/')

@csrf_protect
def login_user(request):
    if request.method == 'GET':
        return render(request, 'register/login.html', {'login_form': AuthenticationForm()})
    elif request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))

            if auth:
                login(request, auth)
                isAdmin = AdminUsers.objects.filter(user=auth)
                print("authentic")
                if not isAdmin.exists():
                    return render(request, 'payapp/home.html', {'success': True, 'user': auth})
                elif isAdmin.exists():
                    return render (request, 'adminStuff/adminHome.html', {'success': True})

            else:
                ##idk if i need to limit the number of tries but this is where it would be
                print("user login combo does not exist")
                return render(request, 'register/login.html', {'success':"User account not valid please try again", 'login_form': AuthenticationForm()})
        else:
            print("form invalid")
            return render(request, 'register/login.html', {'success':"request not valid", "login_form":AuthenticationForm()})
    else:
        print("howve you got here, not a GET or POST request")

@csrf_protect
def logout_user(request):
    if request.method == 'GET':
        django.contrib.auth.logout(request)
        return render(request, 'register/login.html', {'success':"successfully logged out"})
    else:
        return render(request, 'register/login.html', {'success':"how did you get here?"})