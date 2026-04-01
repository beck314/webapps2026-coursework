from _pyrepl.commands import home

from django.db import transaction, DatabaseError, models
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist

from payapp.forms import ExchangeForm
from payapp.models import Notifications, Balance, Transactions, Event_Type


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
                    transferRequest = Notifications(name=asking_username, username=giving_username, amount_requested=money_to_exchange)
                    transferRequest.save()

                    instance = Transactions(user="asking_username", other="giving_username", event_type=Event_Type.request, amount=money_to_exchange)
                    instance.save()

                    instancesr = Notifications(name=giving_username, user_requesting=asking_username, amount_requested=money_to_exchange)
                    instancesr.save()

                return render(request, "payapp/home.html", {'info':"The user will be notified of your request"})

            except (DatabaseError, ObjectDoesNotExist) as e:
                return render(request, "payapp/home.html", {'info': "An error occured while processing your request, the recipient of the request may not exist"})
        else:
            return render(request, "payapp/home.html", {"info": "Your form was invalid, please check your input"})

    else :
        return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})

def sendpayment(request):
    if request.method == "POST":
        ##just send money straight away
        form = ExchangeForm(request.POST)
        if form.is_valid():
            try:
                src_username = form.cleaned_data["enter_your_username"]
                dst_username = form.cleaned_data["enter_destination_username"]
                money_to_transfer = form.cleaned_data["enter_points_to_transfer"]

                src_balance = Balance.objects.select_for_update().get(name__username=src_username)
                dst_balance = Balance.objects.select_for_update().get(name__username=dst_username)

                with transaction.atomic():
                    src_balance.money = src_balance.money - money_to_transfer
                    src_balance.save()

                    dst_balance.money = dst_balance.money + money_to_transfer
                    dst_balance.save()

                    instance = Transactions(name=src_username, other=dst_username, event_type=Event_Type.sent_payment, amount=money_to_transfer)
                    instance.save()

                return render(request, "payapp/home.html", {"src_points": src_balance, "dst_points": dst_balance})
            except (DatabaseError, ObjectDoesNotExist) as e:
                return render(request, "payapp/sendPayment.html", {"form": form, "Error": e})
    else:
        return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})

def transactions(request):#
    if request.method == "POST":
        transaction_list = Transactions.objects.all()
        return render(request, "payapp/transactions.html", {"transactions": transaction_list})
    return

def notifications(request):
    if request.method == "GET":
        request_list = Notifications.objects.all()
        return render(request, "payapp/notifications.html", {"notifications": request_list})
    return

def payapp(request):
    if request.method == 'POST':
        if request.POST.get("next_page") == "request":
            return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})
        elif request.POST.get("next_page") == "send":
            return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})
        elif request.POST.get("next_page") == "transactions":
            return render(request, "payapp/transactions.html")
        elif request.POST.get("next_page") == "notifications":
            return render(request, "payapp/notifications.html")
        else:
            return render(request, "payapp/home.html", {"info": "select a page option please"})

    else:
        return render(request, "payapp/home.html")
