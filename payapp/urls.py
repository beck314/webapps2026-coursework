from django.contrib import admin
from django.urls import path, include
from payapp import views as payapp_views
from register import views as register_views


urlpatterns = [
    path('requestpayment/', payapp_views.makerequest),
    path('makepayment/', payapp_views.sendpayment),
    path('transactions/', payapp_views.transactions),
    path('notifications/', payapp_views.notifications),
    path('register/', register_views.register_user),
    path('login/', register_views.login_user),
    path('logout/', register_views.logout_user),
    path('home/', payapp_views.payapp),
    path('', register_views.login_user),
]