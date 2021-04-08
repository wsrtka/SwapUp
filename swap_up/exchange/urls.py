from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('offers/', views.offers, name='offers'),
    path('manage/', views.manage, name='manage')
]