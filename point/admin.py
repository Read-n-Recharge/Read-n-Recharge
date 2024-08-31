from django.contrib import admin
from .models import UserPoint, PointRecord

# Register your models here.


class UserPointAdmin(admin.ModelAdmin):
    list_display = ["user", "total_points"]


class PointRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "action", "timestamp"]


admin.site.register(UserPoint, UserPointAdmin)
admin.site.register(PointRecord, PointRecordAdmin)
