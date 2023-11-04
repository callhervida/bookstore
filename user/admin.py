from django.contrib import admin

from user.models import User, AuthorProfile


class UserAdmin(admin.ModelAdmin):
    search_fields = ('phone_number',)
    list_display = ('id', 'phone_number', 'first_name', 'is_active')


admin.site.register(User, UserAdmin)
admin.site.register(AuthorProfile)
