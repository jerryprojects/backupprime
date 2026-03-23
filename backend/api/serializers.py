"""
Serializers for the PRIME Project Hub API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Project, TeamMember, AccessRequest, Notification


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles."""
    email = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'bio', 'phone', 'department', 'email', 'name']
        read_only_fields = ['id', 'email', 'name']
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information."""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for team members."""
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'email', 'contribution']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for projects."""
    owner = UserSerializer(read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    approved_faculty_count = serializers.SerializerMethodField()
    access_request_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'abstract', 'domains', 'year', 'license',
            'tech_stack', 'status', 'approval_status', 'owner', 'team_members',
            'created_at', 'updated_at', 'approved_faculty_count', 'access_request_count'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'approved_faculty_count']
    
    def get_approved_faculty_count(self, obj):
        return obj.approved_faculty.count()
    
    def get_access_request_count(self, obj):
        return obj.access_requests.filter(status='pending').count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for project with all related information."""
    owner = UserSerializer(read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    approved_faculty = UserSerializer(many=True, read_only=True)
    access_requests = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'abstract', 'domains', 'year', 'license',
            'tech_stack', 'status', 'approval_status', 'owner', 'team_members',
            'approved_faculty', 'access_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_access_requests(self, obj):
        requests = obj.access_requests.all()
        return AccessRequestSerializer(requests, many=True).data


class AccessRequestSerializer(serializers.ModelSerializer):
    """Serializer for access requests."""
    requester = UserSerializer(read_only=True)
    project = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = AccessRequest
        fields = ['id', 'project', 'requester', 'status', 'requested_at', 'responded_at', 'response_message']
        read_only_fields = ['id', 'requested_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications."""
    related_project_title = serializers.CharField(source='related_project.title', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message', 'related_project',
            'related_project_title', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
