from django.urls import path
from django.contrib.auth import views as auth_views

from auths import views

app_name = 'auths'
urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', auth_views.LoginView.as_view(template_name='auths/login.html'), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(template_name='auths/logout.html'), name='logout'),
]