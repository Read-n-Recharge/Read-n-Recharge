from django.contrib import admin
from .models import Task

# Register your models here.


class TaskDisplayAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "deadlines", "details", "complexity", "complete"]


admin.site.register(Task, TaskDisplayAdmin)
