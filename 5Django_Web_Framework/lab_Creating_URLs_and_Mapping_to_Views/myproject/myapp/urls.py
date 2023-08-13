from . import views
from django.urls import path

urlpatterns =[
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path('menu/',views.menu,name="menu"),
    path('book/',views.book,name="book"),
]