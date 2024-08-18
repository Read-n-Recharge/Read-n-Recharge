from django.contrib import admin
from .models import UserPoint, PointRecord

# Register your models here.


class UserPointAdmin(admin.ModelAdmin):
    list_display = ["user", "total_points"]
    search_fields = ("user__username",)


class PointRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "action", "timestamp"]


admin.site.register(UserPoint, UserPointAdmin)
admin.site.register(PointRecord, PointRecordAdmin)
