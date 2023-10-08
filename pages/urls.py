from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('coding/', views.coding, name='coding'),
    path('explaining/', views.explaining, name='explaining'),
    path('about/', views.about, name='about'),
]