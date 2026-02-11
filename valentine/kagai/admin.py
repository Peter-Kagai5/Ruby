from django.contrib import admin
from .models import UserProfile, LoveNote, Connection, Favorite

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'gender', 'created_at']
    search_fields = ['user__username', 'location', 'bio']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LoveNote)
class LoveNoteAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'status', 'is_anonymous', 'created_at']
    list_filter = ['status', 'is_anonymous', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'content']
    readonly_fields = ['created_at', 'sent_at', 'opened_at']

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user1__username', 'user2__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'note', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
