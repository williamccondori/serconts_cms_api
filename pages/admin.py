from django.contrib import admin

# Register your models here.

from .models import Page, Comment

admin.site.register(Page)

admin.site.register(Comment)