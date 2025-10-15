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
    first_name = serializers.CharField(source="user.profile.first_name", read_only=True)
    last_name = serializers.CharField(source="user.profile.last_name", read_only=True)
    degree = serializers.CharField(source="user.profile.degree", read_only=True)
    gpa = serializers.FloatField(source="user.profile.gpa", read_only=True)
    job_position_display = serializers.CharField(source="job_position.get_title_display", read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "job_position",
            "job_position_display",
            "registered_at",
            "group",
            "first_name",
            "last_name",
            "degree",
            "gpa",
        ]
        read_only_fields = ["registered_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        job_position = validated_data["job_position"]

        if not job_position.is_open():
            raise serializers.ValidationError("This job position is not open for registration.")

        existing = Candidate.objects.filter(user=user).first()
        if existing:
            from datetime import timedelta
            from django.utils import timezone

            delta = timezone.now() - existing.registered_at
            if delta <= timedelta(hours=24):
                existing.job_position = job_position
                existing.save()
                return existing
            raise serializers.ValidationError("The 24-hour deadline for changing the job position has expired.")
        return Candidate.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and not request.user.is_staff and "group" in validated_data:
            validated_data.pop("group")
        return super().update(instance, validated_data)




class CandidateAdminSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.profile.first_name", read_only=True)
    last_name = serializers.CharField(source="user.profile.last_name", read_only=True)
    degree = serializers.CharField(source="user.profile.degree", read_only=True)
    gpa = serializers.FloatField(source="user.profile.gpa", read_only=True)
    job_position_display = serializers.CharField(source="job_position.get_title_display", read_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "job_position",
            "job_position_display",
            "registered_at",
            "group",
            "first_name",
            "last_name",
            "degree",
            "gpa",
        ]
