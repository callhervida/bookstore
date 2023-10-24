from django.contrib import admin

from user.models import User, AuthorProfile

admin.site.register(User)
admin.site.register(AuthorProfile)
