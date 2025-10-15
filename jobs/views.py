from rest_framework import viewsets, permissions
from jobs.models import JobPosition, Candidate
from jobs.serializers import JobPositionSerializer
from jobs.serializers import CandidateSerializer

class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Candidate.objects.all()
        return Candidate.objects.filter(user=user)
