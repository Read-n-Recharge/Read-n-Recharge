from django.contrib import admin
from .models import User, Profile, StudyPrefernce


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
    ]


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ["verified"]
    list_display = ["user", "verified"]


class StudyPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "chronotype",
        "concentration",
        "studying_style",
        "procrastination",
        "physical_activity",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(StudyPrefernce, StudyPreferenceAdmin)
