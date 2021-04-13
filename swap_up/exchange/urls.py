from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('offers/', views.offers, name='offers'),
    path('manage/', views.manage, name='manage'),
    path('offers/add', views.add_offer, name='add-offer'),
    path('add/', views.add_exchange, name='add-exchange'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('download/', views.download_schedule, name='download-csv'),
    path('manage/edit', views.edit_exchange, name='edit-exchange'),
    path('my-offers', views.user_offers, name='user-offers'),
    path('manage/<int:exchange_id>', views.exhange, name='exchange')
]