from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class JobPosition(models.Model):
    JOB_TYPE_CHOICES = (
        ("backend", "Back-end Developer"),
        ("frontend", "Front-end Developer"),
        ("devops", "DevOps Engineer"),
        ("uiux", "UI/UX Designer"),
        ("pm", "Project Manager"),
    )

    title = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def is_open(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["start_time"]


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def can_change_position(self):
        return timezone.now() - self.registered_at <= timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} - {self.job_position.title}"
