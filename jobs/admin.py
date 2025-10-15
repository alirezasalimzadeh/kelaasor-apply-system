# jobs/admin.py
from django.contrib import admin
from jobs.models import JobPosition, Candidate

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start_time", "end_time", "is_open")
    list_filter = ("title",)
    ordering = ("start_time",)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job_position", "registered_at", "group", "degree", "gpa")
    list_filter = ("job_position", "group")
    search_fields = ("user__username", "user__profile__first_name", "user__profile__last_name")

    def degree(self, obj):
        return getattr(obj.user.profile, "degree", "-")

    def gpa(self, obj):
        return getattr(obj.user.profile, "gpa", "-")
