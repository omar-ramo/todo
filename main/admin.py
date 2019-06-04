from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_on', 'finished_on', 'do_before', 'done']
    list_filter = ['done', 'created_on', 'finished_on']
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title', )}
