"""
URL configuration for the API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    UserViewSet, UserProfileViewSet, ProjectViewSet,
    TeamMemberViewSet, AccessRequestViewSet, NotificationViewSet,
    custom_auth_token
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'team-members', TeamMemberViewSet, basename='team-member')
router.register(r'access-requests', AccessRequestViewSet, basename='access-request')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', custom_auth_token, name='custom_token_auth'),
    path('auth/', include('rest_framework.urls')),
]
