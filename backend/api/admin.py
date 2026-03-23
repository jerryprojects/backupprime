from django.contrib import admin
from .models import UserProfile, Project, TeamMember, AccessRequest, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'department']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'approval_status', 'year', 'created_at']
    list_filter = ['status', 'approval_status', 'year', 'created_at']
    search_fields = ['title', 'abstract', 'owner__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    filter_horizontal = ['approved_faculty']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'project', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['name', 'email', 'project__title']
    readonly_fields = ['id', 'created_at']


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'project', 'status', 'requested_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['requester__username', 'project__title']
    readonly_fields = ['id', 'requested_at', 'responded_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['id', 'created_at']
