from django.contrib import admin
from .models import JobPosition, Candidate

@admin.register(JobPosition)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


admin.site.register(Candidate)
