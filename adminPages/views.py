from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, DatabaseError
from django.shortcuts import render

from adminPages.forms import new_admin_form
from adminPages.models import AdminUsers
from payapp.models import Transactions

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if AdminUsers.objects.filter(user=request.user.username):
            ##serve admin webpages
            allTransactions = Transactions.objects.all()
            allUsers = User.objects.all()
            render(request, "adminStuff/adminHome.html", {"transactions": allTransactions, "users": allUsers})
    else:
        ##denied
        render(request, "register/login.html")

def addAdmin(request):
    if request.user.is_authenticated and AdminUsers.objects.filter(user=request.user.username):
        if request.method == "POST":
            form = new_admin_form(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        newAdmin = AdminUsers(user=request.user)
                        newAdmin.save()
                        return render(request, "adminStuff/adminHome.html", {"info": "new admin user added"})
                except (DatabaseError, ObjectDoesNotExist) as e:
                    return render(request, "payapp/home.html", {"info": e})
            else:
                return render(request, "payapp/home.html", {"info": "form not valid"})
        else:
            render(request, "adminStuff/addAdmin.html", {"form": new_admin_form()})

    else:
        render(request, "register/login.html")