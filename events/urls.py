from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eventos/', views.list_events, name='list_events'),

]
