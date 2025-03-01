from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'created_at', 'owner')
    list_filter = ('completed', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    readonly_fields = ('created_at',)
