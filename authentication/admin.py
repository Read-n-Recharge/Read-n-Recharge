from django.contrib import admin
from .models import User,Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','first_name', 'last_name',]


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user','verified']

admin.site.register(User, UserAdmin)
admin.site.register( Profile,ProfileAdmin)