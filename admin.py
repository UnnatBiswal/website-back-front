from django.contrib import admin
from django.db import IntegrityError
from .models import Comment, Scripture, ScriptureImage, Chapter

# Registering Comment model with its admin interface
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', )  # Display these fields in the list view
    search_fields = ('text',)           # Enable search by text field

# Registering Chapter model with its admin interface
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError:
            # If IntegrityError occurs (e.g., duplicate chapter title), display error message
            form.add_error(None, "A chapter with this title already exists in this scripture.")
            return super().response_change(request, obj)

# Registering Scripture model with its admin interface
@admin.register(Scripture)
class ScriptureAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError:
            # If IntegrityError occurs (e.g., duplicate scripture title), display error message
            form.add_error(None, "A scripture with this title already exists.")
            return super().response_change(request, obj)

# Registering ScriptureImage model with its admin interface
admin.site.register(ScriptureImage)
