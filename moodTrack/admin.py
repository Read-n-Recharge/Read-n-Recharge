from django.contrib import admin
from .models import MoodTrack

# Register your models here.


class MoodDisplayAdmin(admin.ModelAdmin):
    list_display = ["user", "mood", "timestamp", "context"]


admin.site.register(MoodTrack, MoodDisplayAdmin)
