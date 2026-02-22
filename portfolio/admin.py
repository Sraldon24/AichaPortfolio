from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import Profile, Skill, Artwork, Message

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('name', 'introduction')
    readonly_fields = ('download_resume_button',)

    def download_resume_button(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" download class="bg-primary-600 border border-transparent font-medium rounded-md text-white px-3 py-2 text-sm hover:bg-primary-700 transition-colors">Download Resume</a>',
                obj.resume.url
            )
        return "No resume uploaded"
    download_resume_button.short_description = "Resume Download"

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ('name',)

@admin.register(Artwork)
class ArtworkAdmin(ModelAdmin):
    list_display = ('title', 'category', 'year', 'completion_date', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')
    list_filter = ('category', 'is_featured', 'year', 'completion_date')
    search_fields = ('title', 'description', 'medium')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ("Basic Information", {
            "fields": ('title', 'slug', 'category', 'medium', 'program', 'dimensions', 'year', 'completion_date', 'order', 'is_featured')
        }),
        ("Images & Media", {
            "fields": ('image', 'image_2', 'image_3', 'image_4', 'video_url', 'video_file')
        }),
        ("Content", {
            "fields": ('description', 'content')
        })
    )

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('name', 'subject', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
