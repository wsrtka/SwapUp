from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('offers/', views.offers, name='offers'),
    path('manage/', views.manage, name='manage'),
    path('manage/edit', views.edit_exchange, name='edit-exchange'),
    path('manage/add', views.add_exchange, name='add-exchange'),
    path('offers/add', views.add_offer, name='add-offer'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('download/', views.download_schedule, name='download-csv'),
    path('schedule/', views.schedule, name='schedule'),
    path('my-offers', views.user_offers, name='user-offers'),
    path('manage/<int:exchange_id>', views.exhange, name='exchange'),
    path('offers/edit', views.edit_offer, name='edit-offer')
]