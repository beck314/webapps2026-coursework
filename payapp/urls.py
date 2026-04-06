from django.contrib import admin
from django.urls import path, include
from payapp import views as payapp_views
from register import views as register_views


urlpatterns = [
    path('requestpayement/', payapp_views.makerequest),
    path('makepayement/', payapp_views.sendpayment),
    path('transactions/', payapp_views.transactions),
    path('notifications/', payapp_views.notifications),
    path('register/', register_views.register_user),
    path('', register_views.login_user),
]