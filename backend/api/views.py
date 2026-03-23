"""
Views for the PRIME Project Hub API.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import UserProfile, Project, TeamMember, AccessRequest, Notification
from .serializers import (
    UserProfileSerializer, UserSerializer, ProjectSerializer,
    ProjectDetailSerializer, TeamMemberSerializer, AccessRequestSerializer,
    NotificationSerializer
)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def custom_auth_token(request):
    """
    Custom token authentication endpoint that accepts email or username.
    """
    email_or_username = request.data.get('email_or_username') or request.data.get('username')
    password = request.data.get('password')
    
    if not email_or_username or not password:
        return Response(
            {'error': 'Please provide email/username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to find user by email first, then by username
    user = User.objects.filter(email=email_or_username).first()
    if not user:
        user = User.objects.filter(username=email_or_username).first()
    
    if not user:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Authenticate user
    authenticated_user = authenticate(username=user.username, password=password)
    if not authenticated_user:
        return Response(
            {'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=authenticated_user)
    
    return Response({
        'token': token.key,
        'user': {
            'id': authenticated_user.id,
            'username': authenticated_user.username,
            'email': authenticated_user.email,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
        }
    })


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permission to allow owners to edit their own projects."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Allow anyone to create a user (signup), but only authenticated users can view details."""
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action == 'me':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticatedOrReadOnly()]
    
    def create(self, request, *args, **kwargs):
        """Create a new user (signup)."""
        data = request.data
        username = data.get('username') or data.get('email')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validate required fields
        if not username or not email or not password:
            return Response(
                {'error': 'username/email, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'email': ['A user with this email already exists']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'username': ['A user with this username already exists']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """Get all projects by a user."""
        user = self.get_object()
        projects = Project.objects.filter(owner=user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profile management."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        """Allow partial updates without authentication for setting role after signup."""
        if self.action in ['partial_update', 'update']:
            return [permissions.IsAuthenticatedOrReadOnly()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user profile."""
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for project management."""
    queryset = Project.objects.all()
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        """Filter projects based on user role and access."""
        user = self.request.user
        if not user.is_authenticated:
            return Project.objects.filter(status='public')
        
        # Admin can see all projects
        if hasattr(user, 'profile') and user.profile.role == 'admin':
            return Project.objects.all()
        
        # Faculty can see public projects and projects they have access to
        if hasattr(user, 'profile') and user.profile.role == 'faculty':
            return Project.objects.filter(
                Q(status='public') | Q(approved_faculty=user)
            ).distinct()
        
        # Students can see all public projects
        return Project.objects.filter(status='public')
    
    def perform_create(self, serializer):
        """Create a new project with the current user as owner."""
        serializer.save(owner=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_projects(self, request):
        """Get projects owned by the current user."""
        projects = Project.objects.filter(owner=request.user)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def request_access(self, request, pk=None):
        """Request access to a locked project."""
        project = self.get_object()
        
        # Check if faculty
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'faculty':
            return Response(
                {'error': 'Only faculty members can request access'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if already has access
        if project.approved_faculty.filter(id=request.user.id).exists():
            return Response(
                {'error': 'You already have access to this project'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or get access request
        access_request, created = AccessRequest.objects.get_or_create(
            project=project,
            requester=request.user
        )
        
        if not created and access_request.status == 'pending':
            return Response(
                {'message': 'Access request already pending'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AccessRequestSerializer(access_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve_access(self, request, pk=None):
        """Owner can approve access for faculty."""
        project = self.get_object()
        
        # Check if user is owner
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can approve access'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        faculty_id = request.data.get('faculty_id')
        if not faculty_id:
            return Response(
                {'error': 'faculty_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        faculty = get_object_or_404(User, id=faculty_id)
        project.approved_faculty.add(faculty)
        
        # Update access request
        access_request = AccessRequest.objects.filter(
            project=project, requester=faculty
        ).first()
        if access_request:
            access_request.status = 'granted'
            access_request.responded_at = timezone.now()
            access_request.save()
            
            # Create notification
            Notification.objects.create(
                user=faculty,
                notification_type='access_granted',
                title='Access Granted',
                message=f'Your access request for "{project.title}" has been approved!',
                related_project=project
            )
        
        serializer = self.get_serializer(project)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def deny_access(self, request, pk=None):
        """Owner can deny access request."""
        project = self.get_object()
        
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can deny access'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        faculty_id = request.data.get('faculty_id')
        if not faculty_id:
            return Response(
                {'error': 'faculty_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access_request = get_object_or_404(
            AccessRequest,
            project=project,
            requester_id=faculty_id
        )
        
        access_request.status = 'rejected'
        access_request.responded_at = timezone.now()
        access_request.response_message = request.data.get('message', '')
        access_request.save()
        
        # Create notification
        Notification.objects.create(
            user=access_request.requester,
            notification_type='access_granted',
            title='Access Request Denied',
            message=f'Your access request for "{project.title}" has been denied.',
            related_project=project
        )
        
        serializer = AccessRequestSerializer(access_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_team_member(self, request, pk=None):
        """Add a team member to the project."""
        project = self.get_object()
        
        if project.owner != request.user:
            return Response(
                {'error': 'Only project owner can add team members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TeamMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def access_requests(self, request, pk=None):
        """Get access requests for a project."""
        project = self.get_object()
        
        if project.owner != request.user and not (
            hasattr(request.user, 'profile') and request.user.profile.role == 'admin'
        ):
            return Response(
                {'error': 'Only project owner or admin can view access requests'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        access_requests = project.access_requests.all()
        serializer = AccessRequestSerializer(access_requests, many=True)
        return Response(serializer.data)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """ViewSet for team member management."""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project', None)
        if project_id:
            return TeamMember.objects.filter(project_id=project_id)
        return TeamMember.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        """Delete a team member."""
        team_member = self.get_object()
        
        if team_member.project.owner != request.user:
            return Response(
                {'error': 'Only project owner can remove team members'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)


class AccessRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for access request management."""
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Users can see requests they made or requests for their projects
        return AccessRequest.objects.filter(
            Q(requester=user) | Q(project__owner=user)
        )


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for notification management."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get notifications for the current user."""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for the user."""
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({'message': f'Marked {notifications.count()} notifications as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count."""
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})
