from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jobs.views import JobPositionViewSet, CandidateViewSet

router = DefaultRouter()
router.register(r'positions', JobPositionViewSet, basename='jobposition')
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = [
    path('', include(router.urls)),
]