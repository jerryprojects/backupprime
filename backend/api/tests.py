"""
Tests for the API app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Project, TeamMember, AccessRequest, Notification


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_created(self):
        """Test that user profile is created when user is created."""
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
    
    def test_default_role_is_student(self):
        """Test that default role is student."""
        profile = self.user.profile
        self.assertEqual(profile.role, 'student')


class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='projowner',
            email='owner@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            abstract='Test abstract',
            owner=self.user,
            year='2024-25'
        )
    
    def test_project_creation(self):
        """Test project creation."""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.owner, self.user)
    
    def test_project_default_status(self):
        """Test default project status is public."""
        self.assertEqual(self.project.status, 'public')


class AccessRequestTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='testpass123'
        )
        self.owner.profile.role = 'student'
        self.owner.profile.save()
        
        self.faculty = User.objects.create_user(
            username='faculty',
            email='faculty@example.com',
            password='testpass123'
        )
        self.faculty.profile.role = 'faculty'
        self.faculty.profile.save()
        
        self.project = Project.objects.create(
            title='Test Project',
            abstract='Test abstract',
            owner=self.owner,
            status='locked'
        )
    
    def test_access_request_creation(self):
        """Test creating an access request."""
        access_request = AccessRequest.objects.create(
            project=self.project,
            requester=self.faculty
        )
        self.assertEqual(access_request.status, 'pending')
