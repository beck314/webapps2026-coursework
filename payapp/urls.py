from django.contrib import admin
from django.urls import path, include
from payapp import views

urlpatterns = [
    path('/requestpayement', views.makerequest),
    path('/makepayement', views.sendpayment),
    path('/transactions', views.transactions),
    path('notifications', views.notifications),
    path('', views),
]