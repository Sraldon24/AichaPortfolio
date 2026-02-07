from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from .models import Profile, Skill, Artwork, Message

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('name', 'introduction')

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

@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ('name', 'subject', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
