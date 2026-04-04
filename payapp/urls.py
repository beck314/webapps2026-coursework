from django.contrib import admin
from django.urls import path, include
from payapp import views as payapp_views
from register import views as register_views


urlpatterns = [
    path('login/', register_views.login_user),
    path('requestpayement/', payapp_views.makerequest),
    path('makepayement/', payapp_views.sendpayment),
    path('transactions/', payapp_views.transactions),
    path('notifications/', payapp_views.notifications),
    path('', payapp_views.payapp),
]