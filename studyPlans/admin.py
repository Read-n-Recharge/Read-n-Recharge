from django.contrib import admin
from .models import Task, StudySession


# Register your models here.


class TaskDisplayAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "deadlines", "details", "complexity", "complete"]

class StudySessionAdmin(admin.ModelAdmin):
    list_filter = ["user","task","studyMethod","stress_level","environment","session_date"]


admin.site.register(Task, TaskDisplayAdmin)
admin.site.register(StudySession, StudySessionAdmin)
