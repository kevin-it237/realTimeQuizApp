from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'quiz'
urlpatterns  = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

