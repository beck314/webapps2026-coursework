from django.contrib.auth.models import User
from django.shortcuts import render

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