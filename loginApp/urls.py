from django.urls import path, include
from . import views

# create namespace
app_name = "loginApp"

# urls
urlpatterns = [
    path('', views.index, name="home"),
    path('myaccount/<int:id>', views.account, name="account"),
    path('myaccount/<int:id>/update', views.accountUpdate, name="accountUpdate"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
]
