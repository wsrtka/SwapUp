from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('upload_shedule', views.upload_shedule, name='upload-shedule')
]