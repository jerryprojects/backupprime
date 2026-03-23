"""
management command to load sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Project, TeamMember, UserProfile
import uuid


class Command(BaseCommand):
    help = 'Load sample data for development'

    def handle(self, *args, **options):
        # Create sample users
        users_data = [
            {'username': 'sarah', 'email': 'sarah@university.edu', 'first_name': 'Sarah', 'last_name': 'Johnson', 'role': 'student'},
            {'username': 'mike', 'email': 'mike@university.edu', 'first_name': 'Mike', 'last_name': 'Chen', 'role': 'student'},
            {'username': 'emma', 'email': 'emma@university.edu', 'first_name': 'Emma', 'last_name': 'Davis', 'role': 'student'},
            {'username': 'faculty_john', 'email': 'john@university.edu', 'first_name': 'John', 'last_name': 'Smith', 'role': 'faculty'},
            {'username': 'admin_user', 'email': 'admin@university.edu', 'first_name': 'Admin', 'last_name': 'User', 'role': 'admin'},
        ]
        
        created_users = {}
        for user_data in users_data:
            role = user_data.pop('role')
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    password='testpass123'
                )
                user.profile.role = role
                user.profile.save()
                created_users[user_data['username']] = user
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
            else:
                created_users[user_data['username']] = User.objects.get(username=user_data['username'])
        
        # Create sample projects
        projects_data = [
            {
                'title': 'AI-Powered Chatbot for Student Support',
                'abstract': 'An intelligent chatbot system using natural language processing to provide 24/7 student support for academic queries, course registration, and campus information.',
                'domains': ['AI', 'NLP'],
                'year': '2024-25',
                'license': 'MIT',
                'tech_stack': ['Python', 'TensorFlow', 'React', 'Node.js'],
                'status': 'public',
                'owner': 'sarah',
                'team_members': [
                    {'name': 'Sarah Johnson', 'email': 'sarah@university.edu', 'contribution': 'ML Model Development & Training'},
                    {'name': 'Mike Chen', 'email': 'mike@university.edu', 'contribution': 'Backend API & Integration'},
                    {'name': 'Emma Davis', 'email': 'emma@university.edu', 'contribution': 'Frontend UI & UX Design'},
                ]
            },
            {
                'title': 'Smart Campus IoT System',
                'abstract': 'A comprehensive IoT solution for monitoring and optimizing campus resources including energy consumption, parking availability, and environmental conditions.',
                'domains': ['IoT', 'Hardware'],
                'year': '2023-24',
                'license': 'Apache 2.0',
                'tech_stack': ['Arduino', 'Raspberry Pi', 'MQTT', 'MongoDB', 'React'],
                'status': 'locked',
                'owner': 'mike',
                'team_members': [
                    {'name': 'Mike Chen', 'email': 'mike@university.edu', 'contribution': 'Hardware Integration & Sensor Development'},
                ]
            },
            {
                'title': 'Blockchain-Based Certificate Verification',
                'abstract': 'A decentralized platform for issuing and verifying academic certificates and credentials using blockchain technology.',
                'domains': ['Blockchain', 'Web'],
                'year': '2024-25',
                'license': 'GPL-3.0',
                'tech_stack': ['Solidity', 'Ethereum', 'Web3.js', 'Next.js', 'TypeScript'],
                'status': 'locked',
                'owner': 'sarah',
                'team_members': [
                    {'name': 'Sarah Johnson', 'email': 'sarah@university.edu', 'contribution': 'Blockchain Development'},
                ]
            },
        ]
        
        for project_data in projects_data:
            owner_username = project_data.pop('owner')
            team_members_data = project_data.pop('team_members')
            owner = created_users[owner_username]
            
            # Generate unique project ID
            project_id = f"proj-{uuid.uuid4().hex[:8]}"
            
            project, created = Project.objects.get_or_create(
                id=project_id,
                defaults={**project_data, 'owner': owner}
            )
            
            if created:
                # Add team members with unique IDs
                for tm_data in team_members_data:
                    tm_id = f"tm-{uuid.uuid4().hex[:8]}"
                    TeamMember.objects.create(
                        id=tm_id,
                        project=project,
                        name=tm_data['name'],
                        email=tm_data['email'],
                        contribution=tm_data['contribution']
                    )
                self.stdout.write(self.style.SUCCESS(f'Created project: {project.title}'))
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
