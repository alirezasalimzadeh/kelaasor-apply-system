from rest_framework import serializers
from jobs.models import JobPosition, Candidate
from datetime import timedelta
from django.utils import timezone


class JobPositionSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField()

    class Meta:
        model = JobPosition
        fields = ["title", "start_time", "end_time", "is_open"]

    def get_is_open(self, obj):
        return obj.is_open()


class CandidateSerializer(serializers.ModelSerializer):
    job_position = serializers.PrimaryKeyRelatedField(queryset=JobPosition.objects.all())

    class Meta:
        model = Candidate
        fields = ["id", "job_position", "registered_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        existing = Candidate.objects.filter(user=user).first()

        if existing:
            delta = timezone.now() - existing.registered_at
            if delta <= timedelta(hours=24):
                existing.job_position = validated_data["job_position"]
                existing.save()
                return existing
            else:
                raise serializers.ValidationError("The 24-hour deadline for changing the job position has expired.")
        else:
            return Candidate.objects.create(user=user, **validated_data)