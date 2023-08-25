from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,api_view
from datetime import datetime
from django.core.paginator import Paginator,EmptyPage
from .models import Menu,Booking
from .serializers import MenuSerializer,BookingSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import BookingForm
import json
from django.core import serializers
# Create your views here.

def index(request):
    return render(request, 'index.html', {})


class BookingViewSet(viewsets.ModelViewSet):
   queryset = Booking.objects.all()
   serializer_class = BookingSerializer
   permission_classes = [IsAuthenticated]


class MenuView(generics.ListCreateAPIView):
    queryset=Menu.objects.all()
    serializer_class= MenuSerializer
    ordering_fields=['price']
    filterset_fields=['price']
    search_fields = ['title']
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return []

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
