from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('offers/', views.offers, name='offers'),
    path('offers/add', views.add_offer, name='add-offer'),
    path('offers/accept/<int:offer_id>', views.accept_offer, name='accept-offer'),
    path('offers/decline/<int:offer_id>', views.decline_offer, name='decline-offer'),
    path('manage/', views.manage, name='manage'),
    path('manage/edit', views.edit_exchange, name='edit-exchange'),
    path('manage/add', views.add_exchange, name='add-exchange'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('download/', views.download_schedule, name='download-csv'),
    path('schedule/', views.schedule, name='schedule'),
    path('my-offers', views.user_offers, name='user-offers'),
    path('manage/<int:exchange_id>', views.exhange, name='exchange')
]