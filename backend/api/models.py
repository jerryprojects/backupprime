"""
Models for the PRIME Project Hub API.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
import uuid as uuid_lib

class UserProfile(models.Model):
    """Extended user profile with role information."""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    


class Project(models.Model):
    """Project model for the hub."""
    STATUS_CHOICES = [
        ('public', 'Public'),
        ('locked', 'Locked'),
        ('approved', 'Approved'),
    ]
    
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    domains = models.JSONField(default=list, help_text="List of project domains/categories")
    year = models.CharField(max_length=20, help_text="Academic year (e.g., 2024-25)")
    license = models.CharField(max_length=100, blank=True)
    tech_stack = models.JSONField(default=list, help_text="List of technologies used")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='public')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_faculty = models.ManyToManyField(User, blank=True, related_name='approved_projects', 
                                             help_text="Faculty members with access to this project")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['owner']),
        ]
    
    def __str__(self):
        return self.title
    

class TeamMember(models.Model):
    """Team member model for projects."""
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contribution = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['project', 'email']
    
    def __str__(self):
        return f"{self.name} - {self.project.title}"


class AccessRequest(models.Model):
    """Access request from faculty to project owner."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('granted', 'Granted'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='access_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    response_message = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['project', 'requester']
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Access Request: {self.requester.username} -> {self.project.title}"


class Notification(models.Model):
    """Notification model for users."""
    TYPE_CHOICES = [
        ('access_request', 'Access Request'),
        ('access_granted', 'Access Granted'),
        ('project_updated', 'Project Updated'),
        ('team_member_added', 'Team Member Added'),
        ('admin_message', 'Admin Message'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=500)
    message = models.TextField()
    related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification: {self.title}"
