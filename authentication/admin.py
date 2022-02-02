from django.contrib import admin
from .models import AppUser

admin.site.register(AppUser)


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'username', 'role')

