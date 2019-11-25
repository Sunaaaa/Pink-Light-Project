from django.urls import path
from django.contrib import admin
from . import views

app_name = 'webserver'
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('<int:train_pk>/', views.detail, name="detail"),
    path('<str:train_no>/train_detail', views.train_detail, name="train_detail"),
    path('<int:train_pk>/edit/', views.edit, name="edit"),
    path('<int:train_pk>/delete/', views.delete, name="delete"),
    path('<int:notification_pk>', views.delete_notification, name="delete_notification"),
    path('<str:train_name>/station_info/', views.station_info, name="station_info"),
    path('<str:station>/station_status', views.station_status, name="station_status"),
    path('<str:seat_info>/pink_light', views.pink_light, name="pink_light"),
]
