from django.contrib import admin

from cookbook.accounts.models import Profile, CbUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user']


@admin.register(CbUser)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password']
