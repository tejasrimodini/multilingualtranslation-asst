from django.contrib import admin
from .models import TranslationHistory

@admin.register(TranslationHistory)
class TranslationHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_language', 'target_language', 'character_count', 'created_at']
    list_filter = ['target_language', 'source_language']
    search_fields = ['source_text', 'translated_text']
    readonly_fields = ['created_at', 'character_count']
    ordering = ['-created_at']
