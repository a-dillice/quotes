from django.urls import path, include
from . import views

# create namespace
app_name = "quoteApp"

# urls
urlpatterns = [
    path('quotes', views.quotes, name="quotes"),
    path('add-quote', views.addQuotes, name="addQuotes"),
    path('delete-quote/<int:id>', views.deleteQuotes, name="deleteQuotes"),
    path('like-quote/<int:id>', views.likeQuotes, name="likeQuotes"),
    path('user/<int:id>', views.userQuotes, name="myQuotes"),
]
