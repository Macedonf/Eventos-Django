from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from events import views
from events.views import list_participantes

urlpatterns = [
    path('', views.index, name='index'),
    path('eventos/', views.list_events, name='list_events'),

    path('<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),

    path('eventos/<int:evento_id>/adicionar/', views.adicionar_participante, name='adicionar_participante'),

    path('evento/<int:evento_id>/participante/<int:participante_id>/editar_participante/', views.editar_participante,name='editar_participante'),

    path('evento/<int:evento_id>/participante/<int:participante_id>/excluir_participante/', views.excluir_participante,name='excluir_participante'),

    path('participantes/<int:evento_id>/',list_participantes, name='list_participantes'),


    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]