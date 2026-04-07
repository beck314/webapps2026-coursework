from _pyrepl.commands import home

from django.contrib.auth.models import User
from django.db import transaction, DatabaseError, models
from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect

from payapp.forms import ExchangeForm
from payapp.models import Notifications, Balance, Transactions, Event_Type


# Create your views here.
@csrf_protect
def makerequest(request):
    if request.method == "POST":
        ##check validity of the form and then send the request to another users account
        ##can be done with notifications model
        form = ExchangeForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                try:
                    asking_user = request.user
                    giving_user = User.objects.filter(username=form.cleaned_data["enter_destination_username"])
                    money_to_exchange = form.cleaned_data["enter_money_to_transfer"]

                    with transaction.atomic():
                        transferRequest = Notifications(user_sending_notif=giving_user, user_receiving_notif=asking_user, amount_requested=money_to_exchange)
                        transferRequest.save()

                        instance = Transactions(user_sending_transaction=asking_user, user_receiving_transaction=giving_user, event_type="rp", amount=money_to_exchange)
                        instance.save()

                    return render(request, "payapp/home.html", {'info':"The user will be notified of your request"})

                except (DatabaseError, ObjectDoesNotExist) as e:
                    return render(request, "payapp/home.html", {'info': "An error occured while processing your request, the recipient of the request may not exist"})
            else:
                return render(request, "payapp/home.html", {"info": "Your form was invalid, please check your input"})
        return render(request, 'register/login.html', {'info': "non authentic user"})
    else :
        return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})

@csrf_protect
def sendpayment(request):
    if request.method == "POST":
        ##just send money straight away
        form = ExchangeForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                try:
                    sender = request.user
                    dst_user = User.objects.get(username = form.cleaned_data["enter_destination_username"])

                    money_to_transfer = form.cleaned_data["enter_money_to_transfer"]

                    src_balance = Balance.objects.select_for_update().get(user=sender)
                    dst_balance = Balance.objects.select_for_update().get(user=dst_user)

                    with transaction.atomic():
                        src_balance.money = src_balance.money - money_to_transfer
                        src_balance.save()

                        dst_balance.money = dst_balance.money + money_to_transfer
                        dst_balance.save()

                        instance = Transactions(user_sending_transaction=sender, user_receiving_transaction=dst_user, event_type='sp', amount=money_to_transfer)
                        instance.save()

                        notif = Notifications(user_sending_notif=sender, user_receiving_notif=dst_user, amount_requested=money_to_transfer)
                        notif.save()

                    return render(request, "payapp/home.html", {"src_balance": src_balance})
                except (DatabaseError, ObjectDoesNotExist) as e:
                    return render(request, "payapp/sendPayment.html", {"form": form, "Error": e})
    else:
        return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})

@csrf_protect
def transactions(request):
    if request.method == "GET":
        user = None
        if request.user.is_authenticated:
            user = request.user
            transaction_list = Transactions.objects.filter(user_sending_transaction=user)
            return render(request, "payapp/transactions.html", {"transactions": transaction_list})
        else:
            return render(request, "register/login.html", {"info": "user not authenticated"})
    else:
        return render(request, "payapp/home.html", {"info": "wrong request method"})

@csrf_protect
def notifications(request):
    if request.method == "GET":
        user = None
        if request.user.is_authenticated:
            user = request.user
            request_list = Notifications.objects.filter(user_receiving_notif=user)
            return render(request, "payapp/notifications.html", {"notifications": request_list})
        else:
            return render(request, "register/login.html", {"info": "user not authenticated"})
    elif request.method == "POST":
        return render(request, "payapp/home.html", {"info": "got to notifications through the wrong pathway"})
    else:
        return render(request, "payapp/home.html", {"info": "Wrong request method"})

@csrf_protect
def payapp(request):
    if request.method == 'POST':
        if request.POST.get("pick_page") == "request payment":
            return render(request, "payapp/requestPayment.html", {"form": ExchangeForm()})
        elif request.POST.get("pick_page") == "send a payment":
            return render(request, "payapp/sendPayment.html", {"form": ExchangeForm()})
        elif request.POST.get("pick_page") == "view past transactions":
            return transactions(request)
        elif request.POST.get("pick_page") == "view notifications":
            return render(request, "payapp/notifications.html")
        else:
            return render(request, "payapp/home.html", {"info": "select a page option please"})

    else:
        balance = Balance.objects.get(user=request.user)
        return render(request, "payapp/home.html", {"info": "Welcome to my payment app", "src_balance": balance.money})
