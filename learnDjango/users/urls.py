from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"   # Я так понимаю что это нужно указывать для пространста имен в urls проекта

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('logout/', views.logout_users, name='logout'),
]
