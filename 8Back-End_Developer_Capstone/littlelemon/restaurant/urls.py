from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
router: DefaultRouter = DefaultRouter()
router.register(r'tables', views.BookingViewSet)
urlpatterns = [
    path('',views.index,name="home"),
    path('book/', views.BookingViewSet.as_view({'get':'list', 'post': 'create', 'delete': 'destroy'}), name="book"),
    path('menu/', views.MenuView.as_view(),name="menu"),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(),name="menu_item"),
    path('bookings/', include(router.urls), name='bookings'),
    path('api-token-auth',obtain_auth_token),
]