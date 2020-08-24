from django.urls import path, include

urlpatterns = [
    path('', include('loginApp.urls')),
    path('', include('quoteApp.urls')),
]