from _pyrepl.commands import home

from django.db import transaction, DatabaseError
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist

from payapp.forms import ExchangeForm
from payapp.models import Notifications


# Create your views here.

def makerequest(request):
    if request.method == "POST":
        ##check validity of the form and then send the request to another users account
        ##can be done with notifications model
        form = ExchangeForm(request.POST)
        if form.is_valid():
            try:
                asking_username = form.cleaned_data["enter_your_username"]
                giving_username = form.cleaned_data["enter_destination_username"]
                money_to_exchange = form.cleaned_data["enter_money_to_transfer"]

                with transaction.atomic():
                    request = Notifications(name=asking_username, username=giving_username, amount_requested=money_to_exchange)
                    request.save()

                return render(request, "payapp/home.html", {{"info":"The user will be notified of your request"}})
            except (DatabaseError, ObjectDoesNotExist) as e:
                return render(request, "payapp/home.html", {"info": "An error occured while processing the form, the recipient of the request may not exist"})
        else:
            return render(request, "payapp/home.html", {"info": "Your form was invalid, please check your input"})

    else :
        return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})

def sendpayment(request):
    if request.method == "POST":
        ##just send money straight away
        return
    else:
        return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})

def transactions(request):#
    if request.method == "GET":
        return render(request, "payapp/transactions.html")
    return

def notifications(request):
    if request.method == "GET":
        return render(request, "payapp/notifications.html")
    return

def payapp(request):
    if request.method == 'POST':
        if request.body.type == "makerequest":
            return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})
        elif request.body.type == "sendpayment":
            return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})
        elif request.body.type == "transactions":
            return render(request, "payapp/transactions.html")
        elif request.body.type == "notifications":
            return render(request, "payapp/notifications.html")
        else:
            return

    else:
        return render(request, "payapp/home.html")
