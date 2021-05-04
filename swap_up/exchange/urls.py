from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='user-home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('offers/', views.offers, name='offers'),
    path('manage/', views.manage, name='manage'),
    path('manage/edit', views.edit_exchange, name='edit-exchange'),
    path('manage/add', views.add_exchange, name='add-exchange'),
    path('offers/add', views.add_offer, name='add-offer'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('download/', views.download_schedule, name='download-csv'),
    path('download-subject/<int:subject_id>', views.download_subject_student_list, name='download-subject'),
    path('schedule/', views.schedule, name='schedule'),
    path('my-offers', views.user_offers, name='user-offers'),
    path('manage/<int:exchange_id>', views.exhange, name='exchange')
]