from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import Profile
from accounts.serializers import RegisterSerializer, ProfileSerializer
from django.contrib.auth.models import User


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)



class MyProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile