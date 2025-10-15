from django.urls import path

from accounts.views import RegisterAPIView, MyProfileAPIView, ProfileAPIView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),

    path("profile/me/", MyProfileAPIView.as_view()),

    path("profile/create/", ProfileAPIView.as_view()),
]
