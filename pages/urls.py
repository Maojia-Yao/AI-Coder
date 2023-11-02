from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('coding/', views.coding, name='coding'),
    path('explaining/', views.explaining, name='explaining'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]