
from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('', views.index, name='index'),
    path('eventos/', views.list_events, name='list_events'),

    path('<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),

    path('eventos/adicionar/', views.adicionar_participante, name='adicionar_participante'),

    path('participantes/', views.list_participantes, name='list_participantes'),

]
