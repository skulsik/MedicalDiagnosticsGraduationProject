from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'owner', 'publication')
    prepopulated_fields = {"slug": ("name",)}
