from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from jobs.models import JobPosition, Candidate
from jobs.serializers import JobPositionSerializer
from jobs.serializers import CandidateSerializer, CandidateAdminSerializer


class JobPositionViewSet(viewsets.ModelViewSet):
    queryset = JobPosition.objects.all()
    serializer_class = JobPositionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def distribute(self, request, pk=None):
        job = self.get_object()
        candidates = (
            Candidate.objects.filter(job_position=job)
            .select_related("user__profile")
            .order_by()
        )

        sorted_list = sorted(
            candidates,
            key=lambda c: (str(getattr(c.user.profile, "degree", "") or ""), -(getattr(c.user.profile, "gpa", 0.0)))
        )

        groups = (1, 2, 3)
        for idx, cand in enumerate(sorted_list):
            cand.group = groups[idx % 3]
            cand.save(update_fields=["group"])

        return Response({"detail": f"Distributed {len(sorted_list)} candidates into 3 groups."},
                        status=status.HTTP_200_OK)



class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Candidate.objects.select_related("user__profile", "job_position")
        return Candidate.objects.select_related("user__profile", "job_position").filter(user=user)



class CandidateAdminViewSet(viewsets.ModelViewSet):

    queryset = Candidate.objects.select_related("user__profile", "job_position")
    serializer_class = CandidateAdminSerializer
    permission_classes = [permissions.IsAdminUser]