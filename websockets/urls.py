from django.urls import path
from . import views

app_name = "websockets"
urlpatterns = [
    path('', views.index, name="index"),
    path('server/', views.server, name="server"),
    path('client/', views.client, name="client"),
]
