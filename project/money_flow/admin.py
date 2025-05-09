from django.contrib import admin
from .models import Status, Type, Category, Note

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'type')
    list_filter = ('type',)
    search_fields = ('name',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'type', 'category', 'total_sum', 'created_at')
    list_filter = ('status', 'type', 'category', 'created_at')
    search_fields = ('comment',)
    autocomplete_fields = ('user', 'status', 'type', 'category')