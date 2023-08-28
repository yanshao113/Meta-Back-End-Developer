from django.shortcuts import render
from rest_framework import generics
from .models import Rating
from .serializers import RatingSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class RatingsView(generics.ListCreateAPIView):
    queryset=Rating.objects.all()
    serializer_class=RatingSerializer
    def get_permission(self):
        if self.request.method=='GET':
            return[]
        return [IsAuthenticated()]