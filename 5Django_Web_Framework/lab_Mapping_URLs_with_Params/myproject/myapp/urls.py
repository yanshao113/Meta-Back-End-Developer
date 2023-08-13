from . import views
from django.urls import path

urlpatterns = [
    path('drinks/<str:drink_name>',views.drinks,name="drink_name"),
]