from django.contrib import admin

from cookbook.accounts.models import Profile, CbUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(CbUser)
class UserAdmin(admin.ModelAdmin):
    pass
