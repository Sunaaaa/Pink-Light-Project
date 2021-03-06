from django.urls import path
from django.contrib import admin
from . import views

app_name = 'webserver'
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new, name="new"),
    path('<int:train_pk>/', views.detail, name="detail"),
    path('<str:train_no>/train_detail', views.train_detail, name="train_detail"),
    path('<str:station>/station_status_detail/<str:train_no>/station_train_detail', views.station_train_detail, name="station_train_detail"),
    path('<int:train_pk>/edit/', views.edit, name="edit"),
    path('<int:train_pk>/delete/', views.delete, name="delete"),
    path('<int:notification_pk>/delete_notification', views.delete_notification, name="delete_notification"),
    path('<str:station>/station_status', views.station_status, name="station_status"),
    path('<str:station>/station_status_detail', views.station_status_detail, name="station_status_detail"),
    path('<str:seat_info>/pink_light', views.pink_light, name="pink_light"),
]
