from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "status", "created_at", "due_date")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")
