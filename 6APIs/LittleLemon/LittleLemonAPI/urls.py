from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:id>',views.single_item),
    path('groups/manager/users',views.managers),
    path('api-token-auth',obtain_auth_token),
    path('groups/manager/users',views.managers),
    path('category',views.categories),
    path('category/<int:id>',views.single_category),
    path('groups/delivery-crew/users',views.delivery_crew),
    path('orders/',views.ordering),
    path('orders/<int:id>',views.single_order),
    path('cart/menu-items/',views.cart)
]